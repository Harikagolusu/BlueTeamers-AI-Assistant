"""
Usage:
    python manage.py backup_db                  # backup all apps
    python manage.py backup_db --apps courses   # backup a single app
    python manage.py backup_db --out /tmp/my_backup.json
"""
import json
from datetime import datetime
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


BACKUP_APPS = [
    "accounts",
    "courses",
    "payments",
    "certificates",
]


class Command(BaseCommand):
    help = "Dump app data to a timestamped JSON file in backups/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apps",
            nargs="+",
            default=BACKUP_APPS,
            help="Apps to back up (default: all)",
        )
        parser.add_argument(
            "--out",
            default=None,
            help="Output file path (default: backups/backup_YYYYMMDD_HHMMSS.json)",
        )

    def handle(self, *args, **options):
        apps = options["apps"]
        out_path = options["out"]

        if not out_path:
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = backup_dir / f"backup_{timestamp}.json"

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        self.stdout.write(f"Backing up: {', '.join(apps)}")

        buf = StringIO()
        call_command(
            "dumpdata",
            *apps,
            indent=2,
            natural_foreign=True,
            natural_primary=True,
            stdout=buf,
        )

        raw = buf.getvalue()
        # Quick sanity check — valid JSON
        data = json.loads(raw)
        out_path.write_text(raw, encoding="utf-8")

        self.stdout.write(
            self.style.SUCCESS(
                f"Backup saved: {out_path}  ({len(data)} objects)"
            )
        )
