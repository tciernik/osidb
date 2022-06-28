# Generated by Django 3.2.13 on 2022-05-16 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("osidb", "0049_misc_models_required_fields_revision"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flaw",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ADOBE", "Adobe"),
                    ("APPLE", "Apple"),
                    ("ASF", "Asf"),
                    ("BIND", "Bind"),
                    ("BK", "Bk"),
                    ("BUGTRAQ", "Bugtraq"),
                    ("BUGZILLA", "Bugzilla"),
                    ("CERT", "Cert"),
                    ("CERTIFI", "Certfi"),
                    ("CORELABS", "Corelabs"),
                    ("CUSTOMER", "Customer"),
                    ("CVE", "Cve"),
                    ("DAILYDAVE", "Dailydave"),
                    ("DEBIAN", "Debian"),
                    ("DISTROS", "Distros"),
                    ("FEDORA", "Fedora"),
                    ("FETCHMAIL", "Fetchmail"),
                    ("FREEDESKTOP", "Freedesktop"),
                    ("FREERADIUS", "Freeradius"),
                    ("FRSIRT", "Frsirt"),
                    ("FULLDISCLOSURE", "Full Disclosure"),
                    ("GAIM", "Gaim"),
                    ("GENTOO", "Gentoo"),
                    ("GENTOOBZ", "Gentoobz"),
                    ("GIT", "Git"),
                    ("GNOME", "Gnome"),
                    ("GNUPG", "Gnupg"),
                    ("GOOGLE", "Google"),
                    ("HP", "Hp"),
                    ("HW_VENDOR", "Hw Vendor"),
                    ("IBM", "Ibm"),
                    ("IDEFENSE", "Idefense"),
                    ("INTERNET", "Internet"),
                    ("ISC", "Isc"),
                    ("ISEC", "Isec"),
                    ("IT", "It"),
                    ("JBOSS", "Jboss"),
                    ("JPCERT", "Jpcert"),
                    ("KERNELBUGZILLA", "Kernelbugzilla"),
                    ("KERNELSEC", "Kernelsec"),
                    ("LKML", "Lkml"),
                    ("LWN", "Lwn"),
                    ("MACROMEDIA", "Macromedia"),
                    ("MAGEIA", "Mageia"),
                    ("MAILINGLIST", "Mailinglist"),
                    ("MILW0RM", "Milw0Rm"),
                    ("MIT", "Mit"),
                    ("MITRE", "Mitre"),
                    ("MOZILLA", "Mozilla"),
                    ("MUTTDEV", "Muttdev"),
                    ("NETDEV", "Netdev"),
                    ("NISCC", "Niscc"),
                    ("", "Novalue"),
                    ("OCERT", "Ocert"),
                    ("OPENOFFICE", "Openoffice"),
                    ("OPENSSL", "Openssl"),
                    ("OPENSUSE", "Opensuse"),
                    ("ORACLE", "Oracle"),
                    ("OSS", "Oss"),
                    ("OSSSECURITY", "Oss Security"),
                    ("PHP", "Php"),
                    ("PIDGIN", "Pidgin"),
                    ("POSTGRESQL", "Postgresql"),
                    ("PRESS", "Press"),
                    ("REAL", "Real"),
                    ("REDHAT", "Redhat"),
                    ("RESEARCHER", "Researcher"),
                    ("RT", "Rt"),
                    ("SAMBA", "Samba"),
                    ("SECALERT", "Secalert"),
                    ("SECUNIA", "Secunia"),
                    ("SECURITYFOCUS", "Securityfocus"),
                    ("SKO", "Sko"),
                    ("SQUID", "Squid"),
                    ("SQUIRRELMAIL", "Squirrelmail"),
                    ("SUN", "Sun"),
                    ("SUNSOLVE", "Sunsolve"),
                    ("SUSE", "Suse"),
                    ("TWITTER", "Twitter"),
                    ("UBUNTU", "Ubuntu"),
                    ("UPSTREAM", "Upstream"),
                    ("VENDORSEC", "Vendor Sec"),
                    ("VULNWATCH", "Vulnwatch"),
                    ("WIRESHARK", "Wireshark"),
                    ("XCHAT", "Xchat"),
                    ("XEN", "Xen"),
                    ("XPDF", "Xpdf"),
                ],
                default="",
                max_length=500,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="flawevent",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ADOBE", "Adobe"),
                    ("APPLE", "Apple"),
                    ("ASF", "Asf"),
                    ("BIND", "Bind"),
                    ("BK", "Bk"),
                    ("BUGTRAQ", "Bugtraq"),
                    ("BUGZILLA", "Bugzilla"),
                    ("CERT", "Cert"),
                    ("CERTIFI", "Certfi"),
                    ("CORELABS", "Corelabs"),
                    ("CUSTOMER", "Customer"),
                    ("CVE", "Cve"),
                    ("DAILYDAVE", "Dailydave"),
                    ("DEBIAN", "Debian"),
                    ("DISTROS", "Distros"),
                    ("FEDORA", "Fedora"),
                    ("FETCHMAIL", "Fetchmail"),
                    ("FREEDESKTOP", "Freedesktop"),
                    ("FREERADIUS", "Freeradius"),
                    ("FRSIRT", "Frsirt"),
                    ("FULLDISCLOSURE", "Full Disclosure"),
                    ("GAIM", "Gaim"),
                    ("GENTOO", "Gentoo"),
                    ("GENTOOBZ", "Gentoobz"),
                    ("GIT", "Git"),
                    ("GNOME", "Gnome"),
                    ("GNUPG", "Gnupg"),
                    ("GOOGLE", "Google"),
                    ("HP", "Hp"),
                    ("HW_VENDOR", "Hw Vendor"),
                    ("IBM", "Ibm"),
                    ("IDEFENSE", "Idefense"),
                    ("INTERNET", "Internet"),
                    ("ISC", "Isc"),
                    ("ISEC", "Isec"),
                    ("IT", "It"),
                    ("JBOSS", "Jboss"),
                    ("JPCERT", "Jpcert"),
                    ("KERNELBUGZILLA", "Kernelbugzilla"),
                    ("KERNELSEC", "Kernelsec"),
                    ("LKML", "Lkml"),
                    ("LWN", "Lwn"),
                    ("MACROMEDIA", "Macromedia"),
                    ("MAGEIA", "Mageia"),
                    ("MAILINGLIST", "Mailinglist"),
                    ("MILW0RM", "Milw0Rm"),
                    ("MIT", "Mit"),
                    ("MITRE", "Mitre"),
                    ("MOZILLA", "Mozilla"),
                    ("MUTTDEV", "Muttdev"),
                    ("NETDEV", "Netdev"),
                    ("NISCC", "Niscc"),
                    ("", "Novalue"),
                    ("OCERT", "Ocert"),
                    ("OPENOFFICE", "Openoffice"),
                    ("OPENSSL", "Openssl"),
                    ("OPENSUSE", "Opensuse"),
                    ("ORACLE", "Oracle"),
                    ("OSS", "Oss"),
                    ("OSSSECURITY", "Oss Security"),
                    ("PHP", "Php"),
                    ("PIDGIN", "Pidgin"),
                    ("POSTGRESQL", "Postgresql"),
                    ("PRESS", "Press"),
                    ("REAL", "Real"),
                    ("REDHAT", "Redhat"),
                    ("RESEARCHER", "Researcher"),
                    ("RT", "Rt"),
                    ("SAMBA", "Samba"),
                    ("SECALERT", "Secalert"),
                    ("SECUNIA", "Secunia"),
                    ("SECURITYFOCUS", "Securityfocus"),
                    ("SKO", "Sko"),
                    ("SQUID", "Squid"),
                    ("SQUIRRELMAIL", "Squirrelmail"),
                    ("SUN", "Sun"),
                    ("SUNSOLVE", "Sunsolve"),
                    ("SUSE", "Suse"),
                    ("TWITTER", "Twitter"),
                    ("UBUNTU", "Ubuntu"),
                    ("UPSTREAM", "Upstream"),
                    ("VENDORSEC", "Vendor Sec"),
                    ("VULNWATCH", "Vulnwatch"),
                    ("WIRESHARK", "Wireshark"),
                    ("XCHAT", "Xchat"),
                    ("XEN", "Xen"),
                    ("XPDF", "Xpdf"),
                ],
                default="",
                max_length=500,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="flawhistory",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ADOBE", "Adobe"),
                    ("APPLE", "Apple"),
                    ("ASF", "Asf"),
                    ("BIND", "Bind"),
                    ("BK", "Bk"),
                    ("BUGTRAQ", "Bugtraq"),
                    ("BUGZILLA", "Bugzilla"),
                    ("CERT", "Cert"),
                    ("CERTIFI", "Certfi"),
                    ("CORELABS", "Corelabs"),
                    ("CUSTOMER", "Customer"),
                    ("CVE", "Cve"),
                    ("DAILYDAVE", "Dailydave"),
                    ("DEBIAN", "Debian"),
                    ("DISTROS", "Distros"),
                    ("FEDORA", "Fedora"),
                    ("FETCHMAIL", "Fetchmail"),
                    ("FREEDESKTOP", "Freedesktop"),
                    ("FREERADIUS", "Freeradius"),
                    ("FRSIRT", "Frsirt"),
                    ("FULLDISCLOSURE", "Full Disclosure"),
                    ("GAIM", "Gaim"),
                    ("GENTOO", "Gentoo"),
                    ("GENTOOBZ", "Gentoobz"),
                    ("GIT", "Git"),
                    ("GNOME", "Gnome"),
                    ("GNUPG", "Gnupg"),
                    ("GOOGLE", "Google"),
                    ("HP", "Hp"),
                    ("HW_VENDOR", "Hw Vendor"),
                    ("IBM", "Ibm"),
                    ("IDEFENSE", "Idefense"),
                    ("INTERNET", "Internet"),
                    ("ISC", "Isc"),
                    ("ISEC", "Isec"),
                    ("IT", "It"),
                    ("JBOSS", "Jboss"),
                    ("JPCERT", "Jpcert"),
                    ("KERNELBUGZILLA", "Kernelbugzilla"),
                    ("KERNELSEC", "Kernelsec"),
                    ("LKML", "Lkml"),
                    ("LWN", "Lwn"),
                    ("MACROMEDIA", "Macromedia"),
                    ("MAGEIA", "Mageia"),
                    ("MAILINGLIST", "Mailinglist"),
                    ("MILW0RM", "Milw0Rm"),
                    ("MIT", "Mit"),
                    ("MITRE", "Mitre"),
                    ("MOZILLA", "Mozilla"),
                    ("MUTTDEV", "Muttdev"),
                    ("NETDEV", "Netdev"),
                    ("NISCC", "Niscc"),
                    ("", "Novalue"),
                    ("OCERT", "Ocert"),
                    ("OPENOFFICE", "Openoffice"),
                    ("OPENSSL", "Openssl"),
                    ("OPENSUSE", "Opensuse"),
                    ("ORACLE", "Oracle"),
                    ("OSS", "Oss"),
                    ("OSSSECURITY", "Oss Security"),
                    ("PHP", "Php"),
                    ("PIDGIN", "Pidgin"),
                    ("POSTGRESQL", "Postgresql"),
                    ("PRESS", "Press"),
                    ("REAL", "Real"),
                    ("REDHAT", "Redhat"),
                    ("RESEARCHER", "Researcher"),
                    ("RT", "Rt"),
                    ("SAMBA", "Samba"),
                    ("SECALERT", "Secalert"),
                    ("SECUNIA", "Secunia"),
                    ("SECURITYFOCUS", "Securityfocus"),
                    ("SKO", "Sko"),
                    ("SQUID", "Squid"),
                    ("SQUIRRELMAIL", "Squirrelmail"),
                    ("SUN", "Sun"),
                    ("SUNSOLVE", "Sunsolve"),
                    ("SUSE", "Suse"),
                    ("TWITTER", "Twitter"),
                    ("UBUNTU", "Ubuntu"),
                    ("UPSTREAM", "Upstream"),
                    ("VENDORSEC", "Vendor Sec"),
                    ("VULNWATCH", "Vulnwatch"),
                    ("WIRESHARK", "Wireshark"),
                    ("XCHAT", "Xchat"),
                    ("XEN", "Xen"),
                    ("XPDF", "Xpdf"),
                ],
                default="",
                max_length=500,
            ),
            preserve_default=False,
        ),
    ]
