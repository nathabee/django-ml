import csv
import glob
import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Creates a CSV file from translation JSON files'

    def handle(self, *args, **kwargs):
        # Define paths
        translations_path = os.path.join(settings.BASE_DIR, 'competence-app/src/demo/data/translation/')
        output_path = os.path.join(settings.BASE_DIR, 'script_db/translation.csv')

        # Open the CSV file for writing
        with open(output_path, mode='w', newline='') as csvfile:
            fieldnames = ['key', 'language', 'translation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Process each JSON file
            for json_file in glob.glob(os.path.join(translations_path, 'translations_*.json')):
                language_code = os.path.splitext(os.path.basename(json_file))[0].split('_')[-1]

                # Load the JSON data
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key, translation in data.items():
                        writer.writerow({
                            'key': key,
                            'language': language_code,
                            'translation': translation
                        })

        self.stdout.write(self.style.SUCCESS(f'Successfully created CSV file at {output_path}'))
