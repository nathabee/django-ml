from django.db import models 
from django.utils import timezone
from django.core.files import File
from PIL import Image
from django.conf import settings
import os


        
# Table: Translation  

class Translation(models.Model):
    key = models.CharField(max_length=255)  # The translation key (e.g. 'welcome')
    language = models.CharField(max_length=10)  # Language code (e.g. 'en', 'fr', etc.)
    translation = models.TextField()  # The translated text

    def __str__(self):
        return f'{self.key} - {self.language}'

    class Meta:
        unique_together = ('key', 'language')  # Ensure unique translations per (key, language)



# Table: Niveau (Class Level & Evaluation Stage)
class Niveau(models.Model):
    niveau = models.CharField(max_length=10)
    description = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['niveau'], name='niveau_idx'),
        ]

    def __str__(self):
        return f"{self.niveau} - {self.description}"


# Table: Etape (Evaluation Stage)
class Etape(models.Model):
    etape = models.CharField(max_length=10)
    description = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['etape'], name='etape_idx'),
        ]

    def __str__(self):
        return f"{self.etape} - {self.description}"


# Table: Annee
class Annee(models.Model):
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    stop_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['is_active'], name='annee_active_idx'),
            models.Index(fields=['start_date'], name='annee_start_date_idx'),
            models.Index(fields=['stop_date'], name='annee_stop_date_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.start_date.year} - {self.description}"


# Table: Matiere
class Matiere(models.Model):
    matiere = models.CharField(max_length=1)
    description = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['matiere'], name='matiere_idx'),
        ]

    def __str__(self):
        return f"{self.matiere} - {self.description}"


# Table: ScoreRule
class ScoreRule(models.Model):
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['description'], name='scorerule_description_idx'),
        ]

    def __str__(self):
        return f"Rule:{self.id} - {self.description}"


# Table: ScoreRulePoint
class ScoreRulePoint(models.Model):
    scorerule = models.ForeignKey('ScoreRule', related_name='points', on_delete=models.CASCADE, default=1)
    scorelabel = models.CharField(max_length=20)
    score = models.IntegerField()
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['scorerule'], name='scorerulepoint_scorerule_idx'),
        ]

    def __str__(self):
        return f"Rule:{self.scorerule.id} - {self.scorelabel} - {self.score} - {self.description}"


# Table: Eleve (Student)
class Eleve(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    niveau = models.ForeignKey('Niveau', on_delete=models.CASCADE, default=1)
    datenaissance = models.DateField(null=True, blank=True)
    professeurs = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='eleves', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['niveau'], name='eleve_niveau_idx'),
        ]

    def __str__(self):
        return f"Eleve:{self.id} - {self.nom} {self.prenom} - {self.niveau}"


# Table: Catalogue (Evaluation Catalog)
class Catalogue(models.Model):
    niveau = models.ForeignKey('Niveau', on_delete=models.CASCADE, default=1)
    etape = models.ForeignKey('Etape', on_delete=models.CASCADE, default=1)
    annee = models.ForeignKey('Annee', on_delete=models.CASCADE, default=1)
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE, default=1)
    description = models.TextField(blank=True, null=True)
    professeurs = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='catalogues', blank=True)
    
    print(f"Catalogue modele", description)

    class Meta:
        indexes = [
            models.Index(fields=['niveau'], name='catalogue_niveau_idx'),
            models.Index(fields=['etape'], name='catalogue_etape_idx'),
            models.Index(fields=['annee'], name='catalogue_annee_idx'),
            models.Index(fields=['matiere'], name='catalogue_matiere_idx'),
        ]

    def __str__(self):
        return f"Catalogue for {self.description}"



# Table: Item (Details for each test in a GroupageData)
class Item(models.Model):
    groupagedata = models.ForeignKey('GroupageData', on_delete=models.CASCADE)
    temps = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    observation = models.TextField(blank=True, null=True)
    scorerule = models.ForeignKey('ScoreRule', on_delete=models.CASCADE, default=1)
    max_score = models.FloatField()
    itempos = models.IntegerField()
    link = models.CharField(max_length=500)

    class Meta:
        indexes = [
            models.Index(fields=['groupagedata'], name='item_groupagedata_idx'),
            models.Index(fields=['scorerule'], name='item_scorerule_idx'),
        ]

    def __str__(self):
        return f"Test {self.groupagedata} - {self.temps} - {self.description}"

 

class MyImage(models.Model):
    icon = models.ImageField(upload_to='competence/icons/')  # Icon image field

    def __str__(self):
        return f"Icone: {self.id}"
 
    def save(self, *args, **kwargs):
        # Check if the image exists before attempting to open or resize it
        if self.pk:
            try:
                previous = MyImage.objects.get(pk=self.pk)
                if previous.icon and previous.icon.path and os.path.exists(previous.icon.path):
                    # Proceed only if the new image is different
                    if previous.icon == self.icon:
                        super(MyImage, self).save(*args, **kwargs)
                        return
            except MyImage.DoesNotExist:
                pass

        # Only resize if the image has changed or is new
        if self.icon and not self.icon.name.startswith('resized_'):
            try:
                img = Image.open(self.icon)  # Open the uploaded image
                img.thumbnail((100, 100), Image.LANCZOS)  # Resize the image

                # Save the resized image
                resized_image_name = f"resized_{os.path.basename(self.icon.name)}"
                temp_file_path = os.path.join(settings.MEDIA_ROOT, 'competence/png/', resized_image_name)

                # Ensure directory exists
                os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

                # Save the resized image to the file system
                img.save(temp_file_path)

                # Update the image field with the resized image
                with open(temp_file_path, 'rb') as f:
                    self.icon.save(resized_image_name, File(f), save=False)

                # Optionally, remove the temporary file after saving the resized image
                os.remove(temp_file_path)

            except Exception as e:
                print(f"Error processing image: {e}")
                pass

        super(MyImage, self).save(*args, **kwargs)


class GroupageData(models.Model):
    catalogue = models.ForeignKey('Catalogue', on_delete=models.CASCADE)
    groupage_icon = models.ForeignKey(MyImage, on_delete=models.SET_NULL, null=True, blank=True)  # FK to MyImage
    position = models.IntegerField()
    desc_groupage = models.CharField(max_length=100)
    label_groupage = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    max_point = models.IntegerField()
    seuil1 = models.IntegerField()
    seuil2 = models.IntegerField()
    max_item = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['catalogue'], name='groupagedata_catalogue_idx'),
        ]

    def __str__(self):
        return f"Groupage {self.desc_groupage} - Position {self.position}"

    def save(self, *args, **kwargs):
        # If the `MyImage` foreign key changes, you don't need to manually resize or change the image.
        # This logic should now be handled in `MyImage.save()`.
        super(GroupageData, self).save(*args, **kwargs)


class PDFLayout(models.Model):
    header_icon = models.ImageField(upload_to='competence/header_icons/')
    schule_name = models.TextField(blank=True, null=True)
    header_message = models.TextField(blank=True, null=True)
    footer_message1 = models.TextField(blank=True, null=True)
    footer_message2 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"PDF Layout: {self.id}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                previous = PDFLayout.objects.get(pk=self.pk)
                if previous.header_icon == self.header_icon:  # Image hasn't changed
                    super(PDFLayout, self).save(*args, **kwargs)
                    return
            except PDFLayout.DoesNotExist:
                pass

        # Only resize if the image has changed or is new
        if self.header_icon and not self.header_icon.name.startswith('resized_'):
            # Open the uploaded image
            img = Image.open(self.header_icon)
            img.thumbnail((100, 100), Image.LANCZOS)

            # Construct the full path for the resized image, including the 'competence/' prefix
            resized_image_name = f"resized_{os.path.basename(self.header_icon.name)}"
            temp_file_path = os.path.join(settings.MEDIA_ROOT, 'competence/header_icons', resized_image_name)
            img.save(temp_file_path)

            # Update the image field with the resized image, ensuring the correct 'competence/' path
            with open(temp_file_path, 'rb') as f:
                # Save with exact name and path without adding any extra string
                self.header_icon.save(f"{resized_image_name}", File(f), save=False)

            # Optionally, remove the temporary file after saving the resized image
            os.remove(temp_file_path)

        super(PDFLayout, self).save(*args, **kwargs)



# Table: Report
class Report(models.Model):
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='reports')
    professeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pdflayout = models.ForeignKey('PDFLayout', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['eleve'], name='report_eleve_idx'),
            models.Index(fields=['professeur'], name='report_professeur_idx'),
        ]

    def __str__(self):
        return f"Report for {self.eleve} - Created by {self.professeur}"


# Table: ReportCatalogue
class ReportCatalogue(models.Model):
    report = models.ForeignKey('Report', on_delete=models.CASCADE, related_name='report_catalogues')
    catalogue = models.ForeignKey('Catalogue', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['report'], name='reportcatalogue_report_idx'),
            models.Index(fields=['catalogue'], name='reportcatalogue_catalogue_idx'),
        ]

    def __str__(self):
        return f"Report Catalogue for {self.catalogue}"


# Table: Resultat
class Resultat(models.Model):
    report_catalogue = models.ForeignKey('ReportCatalogue', on_delete=models.CASCADE, related_name='resultats')
    groupage = models.ForeignKey('GroupageData', on_delete=models.CASCADE)
    score = models.FloatField()
    seuil1_percent = models.FloatField(default=0.0)
    seuil2_percent = models.FloatField(default=0.0)
    seuil3_percent = models.FloatField(default=0.0)

    class Meta:
        indexes = [
            models.Index(fields=['report_catalogue'], name='resultat_report_catalogue_idx'),
            models.Index(fields=['groupage'], name='resultat_groupage_idx'),
        ]

    def __str__(self):
        return f"Resultat for {self.report_catalogue}"


# Table: ResultatDetail
class ResultatDetail(models.Model):
    resultat = models.ForeignKey('Resultat', on_delete=models.CASCADE, related_name='resultat_details')
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    score = models.FloatField()
    scorelabel = models.CharField(max_length=50, blank=True, null=True)
    observation = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['resultat'], name='resultatdetail_resultat_idx'),
            models.Index(fields=['item'], name='resultatdetail_item_idx'),
        ]

    def __str__(self):
        return f"Resultat Detail for {self.resultat}"
