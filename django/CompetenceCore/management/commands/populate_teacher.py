from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from CompetenceCore.models import  Catalogue  
from UserCore.models import CustomUser    
from django.conf import settings 


class Command(BaseCommand):
    help = "Creates users with specified roles and languages."

    def handle(self, *args, **kwargs):
        # Define the user data with roles
        users_data = [
            {'username': 'jacques', 'first_name': 'Jacques', 'last_name': 'Dupain', 'lang': 'fr',  'is_staff': False, 'roles': ['teacher'], 'catalogues': [34, 35, 36]},
            {'username': 'jakob', 'first_name': 'Jakob', 'last_name': 'Brotmann', 'lang': 'de',  'is_staff': False, 'roles': ['teacher'], 'catalogues': [43, 44, 45]},
            {'username': 'jakez', 'first_name': 'Jakez', 'last_name': 'Bara', 'lang': 'br',  'is_staff': False, 'roles': ['teacher'], 'catalogues': [40, 41, 42]},
            {'username': 'james', 'first_name': 'James', 'last_name': 'Breadman', 'lang': 'en',  'is_staff': False, 'roles': ['teacher'], 'catalogues': [37, 38, 39]},
            {'username': 'nathaprof', 'first_name': 'Nathalie', 'last_name': 'Legrand', 'lang': 'fr',  'is_staff': False, 'roles': ['teacher'], 'catalogues': [31, 32, 33]},
            {'username': 'nathachef', 'first_name': 'Nathalie', 'last_name': 'Bordas', 'lang': 'fr', 'is_staff': True, 'roles': ['admin', 'statistics'], 'catalogues': [31, 32, 33]}
        ]

        # Use the default password from settings
        default_password = settings.DEFAULT_USER_PASSWORD

        for user_data in users_data:
            user, user_created = CustomUser.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'lang': user_data['lang'],
                    'is_staff': user_data['is_staff'],
                    'is_active': True,
                }
            )

            if user_created:
                user.set_password(default_password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {user_data['username']}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))

            # Assign roles (groups) to the user
            for role in user_data['roles']:
                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)  # Add the user to each specified group
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created group: {role}"))

            # Save changes to the user after adding groups
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Assigned roles {user_data['roles']} to user: {user_data['username']}"))

            # Associate catalogues with the user (professor)
            for catalogue_id in user_data['catalogues']:
                try:
                    catalogue = Catalogue.objects.get(id=catalogue_id)
                    user.catalogues.add(catalogue)  # Add the catalogue to the user
                    self.stdout.write(self.style.SUCCESS(f"Associated catalogue {catalogue_id} with user: {user_data['username']}"))
                except Catalogue.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Catalogue with id {catalogue_id} not found"))

        self.stdout.write(self.style.SUCCESS("Finished creating users, assigning roles, and associating catalogues."))
