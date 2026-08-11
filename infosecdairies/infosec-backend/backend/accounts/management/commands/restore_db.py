"""
Usage:
    python manage.py restore_db                              # list available backups
    python manage.py restore_db backups/backup_20260503_2305.json
    python manage.py restore_db backups/backup_20260503_2305.json --app courses
"""
from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Load a JSON backup created by backup_db"

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            nargs="?",
            default=None,
            help="Path to the backup JSON file (omit to list available backups)",
        )
        parser.add_argument(
            "--app",
            default=None,
            help="Restore only a specific app label from the fixture",
        )

    def handle(self, *args, **options):
        file_arg = options["file"]

        if not file_arg:
            backup_dir = Path("backups")
            if not backup_dir.exists():
                self.stdout.write("No backups/ directory found.")
                return
            files = sorted(backup_dir.glob("backup_*.json"), reverse=True)
            if not files:
                self.stdout.write("No backup files found in backups/")
                return
            self.stdout.write("Available backups (newest first):")
            for f in files:
                size_kb = f.stat().st_size // 1024
                self.stdout.write(f"  {f}  ({size_kb} KB)")
            self.stdout.write(
                "\nRun:  python manage.py restore_db <file>  to restore one."
            )
            return

        backup_file = Path(file_arg)
        if not backup_file.exists():
            raise CommandError(f"File not found: {backup_file}")

        self.stdout.write(f"Restoring from {backup_file} ...")
        self.stdout.write(self.style.WARNING(
            "WARNING: This will overwrite existing rows with the same primary key."
        ))

        kwargs = {}
        if options["app"]:
            kwargs["app_label"] = options["app"]

        call_command("loaddata", str(backup_file), **kwargs)
        self.stdout.write(self.style.SUCCESS("Restore complete."))
