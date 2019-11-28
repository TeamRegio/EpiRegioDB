from django.contrib import admin
from .models import *

class TableManagerAdmin(admin.ModelAdmin):
    raw_id_fields = ("REMID", 'geneID', 'sampleID')


# Register your models here. So we can access them when logged in as admin
admin.site.register(genomeAnnotation)
admin.site.register(geneExpression)
admin.site.register(sampleInfo)
admin.site.register(cellTypes)
admin.site.register(REMActivity)
admin.site.register(REMAnnotation)
admin.site.register(geneAnnotation)
admin.site.register(CREMAnnotation)



