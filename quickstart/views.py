from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from quickstart.models import Area, Yield, Prod, Harvested
from quickstart.serializers import UserSerializer, GroupSerializer, AreaSerializer, YieldSerializer, ProdSerializer, HarvestedSerializer
from rest_framework import viewsets, views, generics, filters
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_csv.renderers import CSVRenderer, BaseRenderer
from six import StringIO, text_type
import csv, os, numpy, tempfile, zipfile

#import sys, os 
#reload(sys)
#sys.setdefaultencoding('utf-8')

import json
try:
    from six import PY2
except ImportError:
    import sys    
    PY2 = sys.version_info[0] == 2

import re
from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.utils.datastructures import SortedDict
from django.utils.six.moves import range

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from osgeo import gdal, ogr, osr

class CustomPaginatedCSVRenderer(CSVRenderer):
    content_type = 'text/csv'
    format = 'csv'

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

def send_file(request): # Select your file here.  
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for index in range(2):
        filename = __file__ # Select your files here.                           
        archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)

    content = YieldAllViewSet.retrieve()

    return temp

class GeoTIFFRenderer(BaseRenderer):
    media_type = 'image/tiff'
    format = 'geotiff'
    charset = None
    render_style = 'binary'
    headers = None

    def render(self, data, media_type=None, renderer_context=None):
        
        outShapefile = 'test.shp'.encode('utf-8')
        
        driver_ogr = ogr.GetDriverByName('ESRI Shapefile'.encode('utf-8'))
        
        if os.path.exists('test.shp'.encode('utf-8')):
            driver_ogr.DeleteDataSource('test.shp'.encode('utf-8'))

        ds_ogr = driver_ogr.CreateDataSource('test.shp'.encode('utf-8'))

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)

        layer = ds_ogr.CreateLayer('test'.encode('utf-8'), srs, geom_type = ogr.wkbPolygon)
        fieldDefn=ogr.FieldDefn('maiz'.encode('utf-8'), ogr.OFTReal)
        layer.CreateField(fieldDefn)
        
        featureDefn = layer.GetLayerDefn()
        geomcol =  ogr.Geometry(ogr.wkbGeometryCollection)

        for i in data['results']:
            poly = ogr.CreateGeometryFromWkt(i['wkb_geometry'])
            geomcol.AddGeometry(poly)
            feature = ogr.Feature(featureDefn)
            feature.SetGeometry(poly)
            feature.SetField('maiz'.encode('utf-8'), i['maiz'])
            layer.CreateFeature(feature)
            
            poly.Destroy()
            feature.Destroy()

        ds_ogr.Destroy()

        pixel_size = 0.08333333
        NoData_value = -9999

        # Filename of input OGR file
        vector_fn = 'test.shp'.encode('utf-8')

        # Filename of the raster Tiff that will be created
        raster_fn = 'test.tif'.encode('utf-8')

        # Open the data source and read in the extent
        source_ds = ogr.Open(vector_fn)
        source_layer = source_ds.GetLayer()
        source_srs = source_layer.GetSpatialRef()
        x_min, x_max, y_min, y_max = source_layer.GetExtent()

        # Create the destination data source
        x_res = int((x_max - x_min) / pixel_size)
        y_res = int((y_max - y_min) / pixel_size)
        target_ds = gdal.GetDriverByName('GTiff'.encode('utf-8')).Create(raster_fn, x_res, y_res, 1, gdal.GDT_Float32)
        target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
        target_ds.SetProjection(source_srs.ExportToWkt())

        band = target_ds.GetRasterBand(1)
        band.SetNoDataValue(NoData_value)
        # Rasterize
        gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[0], options=["ATTRIBUTE=%s" % 'maiz'.encode('utf-8')])

class YieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Yield.objects.all()
    serializer_class = YieldSerializer

    paginate_by = 20
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomPaginatedCSVRenderer, GeoTIFFRenderer)

    def get_queryset(self):
        queryset = Yield.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

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

'''class YieldAllViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Yield.objects.all()
    serializer_class = YieldSerializer
    paginate_by = None
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer, GeoTIFFRenderer)

    def get_queryset(self):
        queryset = Yield.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset'''

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

class ProdViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Prod.objects.all()
    serializer_class = ProdSerializer

    paginate_by = 20
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomPaginatedCSVRenderer)

    def get_queryset(self):
        queryset = Prod.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset
    
class ProdAllViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Prod.objects.all()
    serializer_class = ProdSerializer
    paginate_by = None
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer)

    def get_queryset(self):
        queryset = Prod.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

class HarvestedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Harvested.objects.all()
    serializer_class = HarvestedSerializer

    paginate_by = 20
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomPaginatedCSVRenderer)

    def get_queryset(self):
        queryset = Harvested.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset
    
class HarvestedAllViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Harvested.objects.all()
    serializer_class = HarvestedSerializer
    paginate_by = None
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer)

    def get_queryset(self):
        queryset = Harvested.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

'''class RouterView(object):
    def __init__(self):
        self.mapping = SortedDict()

    def register(self, *args):
        for regex, view_func in args:
            self.mapping[re.compile(regex)] = view_func

    def __call__(self, request, *args, **kwargs):
        for regex, view_func in self.mapping.items():
            if regex.match(request.path[1:]):
                return view_func(request, *args, **kwargs)
        # does not match
        raise Http404

def some_view(request):
    return HttpResponse('test')

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def some_streaming_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    queryset = Area.objects.all()
    rows = (["Row {0}".format(idx), str(idx)] for idx in range(65536))
    rows = queryset
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response

class TestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    paginate_by = 20
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        queryset = Area.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

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
    serializer_class = GroupSerializer'''
