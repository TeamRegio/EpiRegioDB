"""draftEpi2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import *
from geneQuery.views import *
from geneQuery.views import *
from regionQuery.views import *
from remQuery.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", home_view, name="home-page"),
    path('help/', help_view),
    path('contact/', contact_view),

    path('geneQuery/', geneQuery_view, name='geneQuery-page'),
    path('geneQuery_search/', gene_search_view),
    path('celltype_search', search_cellTypes),
    path('genesymbol_search', search_geneSymbol),
    path('geneQuery_search/gene_details/', gene_details_view),
    path('geneQuery_search/<REMID>/', crem_view, name='crems'),


    path('regionQuery/', regionQuery_view),
    path('regionQuery_search/', region_search_view),

    path('REMQuery/', remQuery_view),
    path('REMQuery_search/', rem_search_view),


    path('navbars/', navbars_view),
]

urlpatterns += staticfiles_urlpatterns()
