from django.conf.urls import url
from . import views #import own view file

urlpatterns = [
	#TODO: create Homeview
#	url(r'^$', views.home, name = 'REST_API_')

	# display all genes: /REST_API/GeneInfo/
#	url(r'^GeneInfo/$', views.GeneInfoAll.as_view(), name = "gene_info_all"),
	#TODO: display link to doc
	#display specific gene:  /REST_API/GeneInfo/GeneId/
	url(r'^GeneInfo/(?P<gene_id>[-\w]+)/$', views.GeneInfo.as_view(), name = "gene_info"),

	#TODO: display link to doc
	#show all REMs: /REST_API/REMs/
#	url(r'^REMs/$', views.REMInfoAll.as_view(), name = "REMs_info_all"),
	#show specific REM: /REST_API/REMQuery/REMID/
	#url(r'^REMs/(?P<REM_id>[A-Za-z0-9]+)/$', views.REMInfo, name = "REM_info"),
	url(r'^REMQuery/(?P<REM_id>[-\w]+)/$', views.REMQuery, name = "REM_info"),

	#CREMInfo: /REST_API/CREMQuery/<CREMID>
	url(r'^CREMQuery/(?P<CREM_id>[-\w]+)/$', views.CREMQuery, name = "CREM_info"),
	
	#GeneQuery: /REST_API/GeneQuery/<GeneID>
	url(r'^GeneQuery/(?P<gene_id>[-\w]+)/$', views.GeneQuery, name = "Gene_info"),

	#RegionQuery: /REST_API/RegionQuery/<chr:start-end>
	url(r'^RegionQuery/(?P<region>[:\-\w]+)/$', views.RegionQuery, name = "Region_info"),
]


