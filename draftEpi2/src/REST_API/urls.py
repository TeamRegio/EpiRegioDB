from django.conf.urls import url
from . import views #import own view file

urlpatterns = [
	# display all genes: /REST_API/GeneInfo/
#	url(r'^GeneInfo/$', views.GenesInfo.as_view(), name = "genes_info"),
	#display specific gene:  /REST_API/GeneInfo/GeneId/
	url(r'^GeneInfo/(?P<gene_id>[A-Z0-9]+)/$', views.GeneInfo.as_view(), name = "gene_info"),

	#show all REMs: /REST_API/REMs/
#	url(r'^REMs/', views.REMsInfo.as_view(), name = "REMs_info"),

	#show specific REM: /REST_API/REMs/REMID/
	url(r'^REMs/(?P<REM_id>[A-Z0-9]+)/$', views.REMInfo.as_view(), name = "REM_info"),
	
]


