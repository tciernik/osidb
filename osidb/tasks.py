import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django_celery_results.models import TaskResult

from config.celery import app

logger = logging.getLogger(__name__)


def get_last_success_for_task(task_name):
    """Return the timestamp of the last successful task so we can fetch updates since that time.

    For extra measure, the last success timestamp is offset by 30 minutes to overlap. If no record
    of a job that succeeded exists in our results DB, return a refresh timestamp of 3 days ago.
    If that still misses stuff, it indicates a longer outage and updates should be scheduled
    manually.
    """
    # Specifically query for jobs without any task kwargs so prevent refreshing only after a
    # successful manually triggered task for a particular resource.
    last_success = (
        TaskResult.objects.filter(task_name=task_name, task_kwargs='"{}"', status="SUCCESS")
        .order_by("-date_done")
        .values_list("date_done", flat=True)
        .first()
    )
    return (
        last_success - timezone.timedelta(minutes=30) if last_success else timezone.now() - timezone.timedelta(days=3)
    )


@app.task(autoretry_for=(Exception,), retry_backoff=900, retry_jitter=False)
def email_failed_tasks():
    """Send email about failed Celery tasks within past 24 hours to OSIDB admins (mailing list)
    If it failed to send, wait 15 minutes and try again, then wait 30 minutes and try again, then give up"""
    failed_tasks_threshold = get_last_success_for_task("osidb.tasks.email_failed_tasks")
    failed_tasks = TaskResult.objects.filter(
        status__exact="FAILURE",
        date_done__gte=failed_tasks_threshold,
    ).order_by("task_name", "date_done")

    subject = f"Failed OSIDB Celery tasks after {failed_tasks_threshold.date()}: {failed_tasks.count()}"

    failed_tasks = "\n".join(
        f"{task.task_name}: args={task.task_args}, kwargs={task.task_kwargs}\nresult={task.result}\n{task.traceback}\n"
        for task in failed_tasks
    )

    email = EmailMessage(
        subject=subject,
        body=failed_tasks,
        to=settings.ADMINS,
        from_email=settings.SERVER_EMAIL,
    )
    email.send()


@app.task
def expire_task_results():
    """Delete task results older than 30 days.

    To prevent the task results table to grow to huge numbers, remove any results that are
    30 days or older. This job mimics the built-in celery.backend_cleanup job but works with
    our schedules and is a bit more transparent in what it actually does.
    """
    expired_on = timezone.now() - timezone.timedelta(days=30)
    removed_count, _ = TaskResult.objects.filter(date_done__lt=expired_on).delete()
    logger.info("Removed %s expired task results", removed_count)

    return f"Removed {removed_count} expired task results"
