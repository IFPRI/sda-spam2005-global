from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from quickstart.models import Area
from quickstart.serializers import UserSerializer, GroupSerializer, AreaSerializer
from rest_framework import viewsets, views, generics, filters
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_csv.renderers import CSVRenderer
from six import StringIO, text_type
import csv
import json
try:
    from six import PY2
except ImportError:
    import sys    
    PY2 = sys.version_info[0] == 2

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CustomCSVRenderer(CSVRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if data is None:
            return ''

        if not isinstance(data, list):
            data = [data]

        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        # Write header
        for elem in data[0].keys():
            print elem
        csv_writer.writerow([
                elem.encode('utf-8') if isinstance(elem, text_type) and PY2 else elem
                for elem in data[0].keys()
            ])
        for row in data:
            # Assume that strings should be encoded as UTF-8
            csv_writer.writerow([
                elem.encode('utf-8') if isinstance(elem, text_type) and PY2 else elem
                for elem in row.values()
            ])

        return csv_buffer.getvalue()

class CustomPaginatedCSVRenderer(CSVRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if data is None:
            return ''

        if not isinstance(data, list):
            data = [data]

        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        # Write header
        for elem in data[0]['results'][0].keys():
            print elem
        csv_writer.writerow([
                elem.encode('utf-8') if isinstance(elem, text_type) and PY2 else elem
                for elem in data[0]['results'][0].keys()
            ])
        for row in data[0]['results']:
            # Assume that strings should be encoded as UTF-8
            csv_writer.writerow([
                elem.encode('utf-8') if isinstance(elem, text_type) and PY2 else elem
                for elem in row.values()
            ])

        return csv_buffer.getvalue()

class AreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    paginate_by = 20
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomPaginatedCSVRenderer)

    def get_queryset(self):
        queryset = Area.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

class AreaAllViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    paginate_by = None
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer)

    def get_queryset(self):
        queryset = Area.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset
    