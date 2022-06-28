"""
Bugzilla collector celery tasks
"""
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from collectors.framework.models import collector

from .collectors import BzTrackerCollector, FlawCollector

logger = get_task_logger(__name__)


@collector(
    base=FlawCollector,
    crontab=crontab(),
    depends_on=["collectors.product_definitions.tasks.product_definitions_collector"],
)
def flaw_collector(collector_obj):
    """bugzilla flaw collector"""
    logger.info(f"Collector {collector_obj.name} is running")
    return collector_obj.collect()


@collector(
    base=BzTrackerCollector,
    crontab=crontab(),
    depends_on=["collectors.bzimport.tasks.flaw_collector"],
)
def bztracker_collector(collector_obj):
    logger.info(f"Collector {collector_obj.name} is running")
    return collector_obj.collect()
