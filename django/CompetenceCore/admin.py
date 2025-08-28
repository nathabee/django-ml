from django.contrib import admin 
from django.utils.html import format_html
from .models import Niveau, Etape, Annee, Matiere, ScoreRule, ScoreRulePoint, Eleve, Catalogue, GroupageData, Item, \
                    PDFLayout, Report, ReportCatalogue, Resultat, ResultatDetail, MyImage ,Translation

import base64 
  
from .forms import ImagePreviewWidget ,GroupageDataForm   #, IconPreviewSelect 
from django.utils.safestring import mark_safe
   
 
 
# Inline classes
class ResultatDetailInline(admin.TabularInline):
    model = ResultatDetail
    extra = 1

class ResultatInline(admin.TabularInline):
    model = Resultat
    extra = 1
    inlines = [ResultatDetailInline]

class ReportCatalogueInline(admin.TabularInline):
    model = ReportCatalogue
    extra = 1
    inlines = [ResultatInline]

 


# Define a custom filter class
class KeyPrefixFilter(admin.SimpleListFilter):
    title = 'Key Prefix (First 3 Letters)'  # Display title for the filter
    parameter_name = 'key_prefix'  # Internal name of the filter

    def lookups(self, request, model_admin):
        # Gather all unique first-three-letter prefixes
        prefixes = set([translation.key[:3] for translation in Translation.objects.all()])
        return [(prefix, prefix) for prefix in prefixes]

    def queryset(self, request, queryset):
        # Apply the filter to the queryset
        if self.value():
            return queryset.filter(key__startswith=self.value())
        return queryset

# Register the Translation model with the custom filter
@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('key', 'language', 'translation')
    search_fields = ('key', 'language')
    list_filter = (KeyPrefixFilter,)  # Include the custom filter
 

@admin.register(GroupageData)
class GroupageDataAdmin(admin.ModelAdmin):
    form = GroupageDataForm  # Use the custom form

    list_display = ('catalogue', 'display_groupage_icon', 'position', 'desc_groupage', 'label_groupage', 'link', 'max_point', 'seuil1', 'seuil2', 'max_item')
    list_filter = ('catalogue',)
    search_fields = ('desc_groupage', 'label_groupage', 'link')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['groupage_icon'].widget.attrs.update({
            'onchange': 'updateImagePreview(this);'  # Call the JavaScript function on change
        })
        return form
    
 

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        current_image_url = None
        my_images = MyImage.objects.all()  # Fetch all images for the dropdown

        if obj:
            current_image_url = obj.groupage_icon.icon.url if obj.groupage_icon and obj.groupage_icon.icon else None

        return super().change_view(request, object_id, form_url, extra_context={
            'current_image_url': current_image_url,
            'my_images': my_images,
        })

    def display_groupage_icon(self, obj):
        """Display a small icon preview in the list display."""
        if obj.groupage_icon_id:
            try:
                my_image = MyImage.objects.get(pk=obj.groupage_icon_id)
                if my_image.icon:
                    return format_html('<img src="{}" style="width: 30px; height: 30px;"/>', my_image.icon.url)
            except MyImage.DoesNotExist:
                return "Image not found"
        return "-"

    display_groupage_icon.short_description = "Groupage Icon"
 

@admin.register(MyImage)
class MyImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_icon']  # Ensure 'display_icon' is referenced here
    search_fields = ['id', 'icon']  # Allows search by ID and icon file name

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Customize the form field for the 'icon' to include the preview."""
        if db_field.name == 'icon':  # Assuming 'icon' is your image field
            kwargs['widget'] = ImagePreviewWidget  # Use the custom preview widget
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def display_icon(self, obj):
        """Displays a small icon preview in the list display."""
        if obj.icon:
            return format_html('<img src="{}"  style="max-height: 200px; max-width: 100%; height: auto; width: auto; object-fit: contain;" />', obj.icon.url)
        return "-"  # Return a placeholder if no icon is available

    display_icon.short_description = "Icon"  # Optional: Sets the column header name


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('niveau', 'description')
    list_filter = ('niveau',)
    search_fields = ('niveau', 'description')

@admin.register(Etape)
class EtapeAdmin(admin.ModelAdmin):
    list_display = ('etape', 'description')
    list_filter = ('etape',)
    search_fields = ('etape', 'description')

@admin.register(Annee) 
class AnneeAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'start_date', 'stop_date', 'description')  # Replace 'annee' with valid fields
 

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('matiere', 'description')
    search_fields = ('matiere', 'description')

@admin.register(ScoreRule)
class ScoreRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')
    search_fields = ('description',)

@admin.register(ScoreRulePoint)
class ScoreRulePointAdmin(admin.ModelAdmin):
    list_display = ('scorerule', 'scorelabel', 'score', 'description')
    list_filter = ('scorerule',)
    search_fields = ('scorelabel', 'description')



@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'niveau')
    search_fields = ('nom', 'prenom', 'niveau')
    filter_horizontal = ('professeurs',)  # For ManyToMany fields

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ('niveau', 'etape', 'annee', 'matiere', 'description')
    list_filter = ('niveau', 'etape', 'annee', 'matiere')
    ordering = ('niveau', 'etape')

    search_fields = ('description',)
    filter_horizontal = ('professeurs',)  # For ManyToMany fields


#@admin.register(GroupageData)
#class GroupageDataAdmin(admin.ModelAdmin):
 ##   list_display = ('catalogue', 'display_groupage_icon', 'position', 'desc_groupage', 'label_groupage', 'link', 'max_point', 'seuil1', 'seuil2', 'max_item')
 #   list_filter = ('catalogue',)
 #   autocomplete_fields = ['groupage_icon']  # References MyImage and requires search_fields
 #   search_fields = ('desc_groupage', 'label_groupage', 'link', 'groupage_icon__icon')  # Note the double underscore for the related field
##
 #   def formfield_for_foreignkey(self, db_field, request, **kwargs):
 #       if db_field.name == "groupage_icon":
 #           kwargs['widget'] = IconPreviewWidget
 #       return super().formfield_for_foreignkey(db_field, request, **kwargs)#

    #def display_groupage_icon(self, obj):
    #    if obj.groupage_icon and hasattr(obj.groupage_icon, 'url'):
    #        try:
    #            return format_html('<img src="{}" style="width: 30px; height: 30px;"/>', obj.groupage_icon.icon.url)
    #        except FileNotFoundError:
    #            return "Image not found"
    #    return "-"
    
    #display_groupage_icon.short_description = "Groupage Icon"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'temps', 'max_score', 'itempos')  # Customize fields to display
    list_filter = ('groupagedata',)  # Allows filtering by groupagedata
    search_fields = ('description', 'temps')  # Enable search by description and temps

 



@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'professeur', 'created_at', 'updated_at')
    list_filter = ('professeur', 'created_at')
    search_fields = ('eleve__nom', 'eleve__prenom')

    inlines = [ReportCatalogueInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('eleve', 'professeur').prefetch_related(
            'report_catalogues__catalogue',
            'report_catalogues__resultats__resultat_details'
        )
    
    
@admin.register(ReportCatalogue)
class ReportCatalogueAdmin(admin.ModelAdmin):
    list_display = ('report', 'catalogue')
    list_filter = ('report',)
    search_fields = ('report__eleve__nom', 'catalogue__description')

@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('report_catalogue', 'groupage', 'score')
    list_filter = ('report_catalogue',)
    search_fields = ('report_catalogue__report__eleve__nom',)

@admin.register(ResultatDetail)
class ResultatDetailAdmin(admin.ModelAdmin):
    list_display = ('resultat', 'item', 'score')
    list_filter = ('resultat', 'item')
    search_fields = ('resultat__report_catalogue__report__eleve__nom', 'item__description')

 
 

@admin.register(PDFLayout)
class PDFLayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_header_icon', 'schule_name', 'header_message', 'footer_message1', 'footer_message2')
    search_fields = ('header_icon', 'schule_name', 'header_message', 'footer_message1', 'footer_message2')

    def display_header_icon(self, obj):
        if obj.header_icon:
            with open(obj.header_icon.path, 'rb') as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                return format_html('<img src="data:image/png;base64,{}" style="width: 50px; height: 50px;"/>', encoded_string)
        return "-"
    
    display_header_icon.short_description = "Header Icon"

