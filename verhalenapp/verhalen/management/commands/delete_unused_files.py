import os
from django.core.management.base import BaseCommand
from django.conf import settings
from verhalen.models import Verhaal
from verhalen.models import Categorie 
from overmijpagina.models import Overmij

class Command(BaseCommand):
    help = "Deletes unused images from media/ that are not referenced by any models."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview which files would be deleted, but don’t actually delete them.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        media_root = settings.MEDIA_ROOT

        if not os.path.exists(media_root):
            self.stdout.write(self.style.ERROR("MEDIA_ROOT does not exist."))
            return

        # Collect all media files
        all_files = set()
        for root, _, files in os.walk(media_root):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, media_root)
                all_files.add(relative_path)

        # Collect used files
        used_files = set()
        for obj in Verhaal.objects.all():
            if obj.pdf_file:
                used_files.add(obj.pdf_file.name)
            if obj.word_file:
                used_files.add(obj.word_file.name)
            if obj.cover_image:
                used_files.add(obj.cover_image.name)

        for cat in Categorie.objects.all():
            if cat.cover_image:
                used_files.add(cat.cover_image.name)

        for bio in Overmij.objects.all():
            if bio.afbeelding:
                used_files.add(bio.afbeelding.name)

        unused_files = all_files - used_files

        if not unused_files:
            self.stdout.write(self.style.SUCCESS("No unused media files found."))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run mode — files to be deleted:"))
            for f in sorted(unused_files):
                self.stdout.write(f" - {f}")
        else:
            deleted_count = 0
            for f in unused_files:
                file_path = os.path.join(media_root, f)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_count += 1
                    self.stdout.write(f"Deleted: {f}")
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} files."))
