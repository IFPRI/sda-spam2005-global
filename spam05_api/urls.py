# from django.contrib import admin
# admin.autodiscover()

from django.conf.urls import patterns, url, include
from rest_framework import routers
from quickstart import views

from django.http import HttpResponse
from quickstart.views import RouterView, some_view, some_streaming_csv_view, send_file

routerRaw = RouterView()
routerRaw.register(
	(r'^foo/test', some_view),
    (r'^foo/area_all', some_streaming_csv_view),
    (r'^foo/download', send_file),
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'area', views.AreaViewSet)
router.register(r'area_all', views.AreaAllViewSet)
router.register(r'yield', views.YieldViewSet)
router.register(r'yield_all', views.YieldAllViewSet)
router.register(r'prod', views.ProdViewSet)
router.register(r'prod_all', views.ProdAllViewSet)
router.register(r'harvested', views.HarvestedViewSet)
router.register(r'harvested_all', views.HarvestedAllViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
	url(r'^foo/', routerRaw),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

# import autocomplete_light
# import every app/autocomplete_light_registry.py
# autocomplete_light.autodiscover()

#import admin
#admin.autodiscover()