import os
from django.core.management.base import BaseCommand
from django.conf import settings
from verhalen.models import Categorie 

class Command(BaseCommand):
    help = "Deletes unused images from verhalen_covers/ that are not referenced by Verhaal.cover_image"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview which files would be deleted, but don’t actually delete them.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']


        covers_dir = os.path.join(settings.MEDIA_ROOT, 'categorie_covers')

        if not os.path.exists(covers_dir):
            self.stdout.write(self.style.ERROR("verhalen_covers directory does not exist in MEDIA_ROOT."))
            return


        all_files = set()
        for root, dirs, files in os.walk(covers_dir):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, settings.MEDIA_ROOT)
                all_files.add(relative_path)


        used_files = set()
        for obj in Categorie.objects.all():  
            if obj.cover_image:              
                used_files.add(obj.cover_image.name)


        unused_files = all_files - used_files

        if not unused_files:
            self.stdout.write(self.style.SUCCESS("No unused images found in categorie_covers/."))
            return

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run mode — no files will be deleted."))
            self.stdout.write("The following files would be deleted:")
            for rel_path in sorted(unused_files):
                self.stdout.write(f" - {rel_path}")
            self.stdout.write(self.style.SUCCESS(f"{len(unused_files)} file(s) would be deleted."))
        else:
            deleted_count = 0
            for rel_path in unused_files:
                full_path = os.path.join(settings.MEDIA_ROOT, rel_path)
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    self.stdout.write(f"Deleted: {rel_path}")
                    deleted_count += 1
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} unused image(s) from categorie_covers/."))
