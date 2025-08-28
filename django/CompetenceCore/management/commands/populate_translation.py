import csv
from django.core.management.base import BaseCommand
from CompetenceCore.models import Translation


class Command(BaseCommand):
    help = 'Populate the Translation table from a CSV file'

    def handle(self, *args, **kwargs):
        csv_path = 'CompetenceCore/script_db/translation.csv'

        # Read CSV and populate database
        with open(csv_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Update or create translation entry
                Translation.objects.update_or_create(
                    key=row['key'],
                    language=row['language'],
                    defaults={'translation': row['translation']}
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the Translation table from CSV'))
