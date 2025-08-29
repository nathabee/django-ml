# django/CompetenceCore/management/commands/copy_data_init.py
import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
 


    help = 'Copy file data from script_db/competence into media origin'
 

    def handle(self, *args, **kwargs):


        # Define the source and destination directories
        src_dir = 'CompetenceCore/script_db/competence'
        dest_dir = '/var/www/competence_project/media/origin'

        # Check if the destination directory exists and has write permission
        if os.path.exists(dest_dir) and os.access(dest_dir, os.W_OK):
            self.stdout.write(self.style.SUCCESS(f'Target directory {dest_dir} exists and is writable.'))
            try:
                # Perform the copy operation
                subprocess.run(['sudo', 'cp', '-r', src_dir, dest_dir], check=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully copied files from {src_dir} to {dest_dir}'))
            except subprocess.CalledProcessError as e:
                self.stderr.write(self.style.ERROR(f'Error copying files: {e}'))
        else:
            # Directory doesn't exist or is not writable
            if not os.path.exists(dest_dir):
                self.stderr.write(self.style.ERROR(f'Target directory {dest_dir} does not exist.'))
            if not os.access(dest_dir, os.W_OK):
                self.stderr.write(self.style.ERROR(f'No write permission for the directory {dest_dir}.'))
            return  # Exit the command if the directory is not writable

