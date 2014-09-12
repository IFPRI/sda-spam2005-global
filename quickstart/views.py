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

def createShapefile(data, filename, fields):
    charset = 'utf-8'
    outShapefile = 'build/' + filename +'.shp'
        
    driver_ogr = ogr.GetDriverByName('ESRI Shapefile'.encode('utf-8'))
        
    if os.path.exists(filename +'.shp'):
        driver_ogr.DeleteDataSource(filename +'.shp'.encode('utf-8'))

    ds_ogr = driver_ogr.CreateDataSource(filename +'.shp'.encode('utf-8'))

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)

    layer = ds_ogr.CreateLayer(filename.encode('utf-8'), srs, geom_type = ogr.wkbPolygon)
    print fields
    for field in fields:
        if (field != 'wkb_geometry'):
            fieldDefn=ogr.FieldDefn(field.encode('utf-8'), ogr.OFTReal)
            layer.CreateField(fieldDefn)
        
    featureDefn = layer.GetLayerDefn()
    geomcol =  ogr.Geometry(ogr.wkbGeometryCollection)

    # for i in data['results']: # this is for paginated response
    for i in data:
        poly = ogr.CreateGeometryFromWkt(i['wkb_geometry'])
        geomcol.AddGeometry(poly)
        feature = ogr.Feature(featureDefn)
        feature.SetGeometry(poly)
        for field in fields:
            if (field != 'wkb_geometry'):
                feature.SetField(field.encode('utf-8'), i[field])
        layer.CreateFeature(feature)
            
        poly.Destroy()
        feature.Destroy()

    ds_ogr.Destroy()

def createGeoTIFF(data, filename, field):
    pixel_size = 0.08333333
    NoData_value = -9999

    # Filename of input Shapefile
    vector_fn = filename + '.shp'.encode('utf-8')

    # Filename of the raster Tiff that will be created
    raster_fn = filename + '.tif'.encode('utf-8')

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
    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[0], options=["ATTRIBUTE=%s" % field.encode('utf-8')])    

def buildFileName(fields, iso3s, variable):
    filename = 'spam2005_' + variable + '_'
    print fields
    filename = filename + fields.replace(',','_').replace('wkb_geometry','').strip('_')
    filename = filename + '_' + iso3s.replace(',','_').strip('_')
    return filename

class ShapefileRenderer(BaseRenderer):
    media_type = 'application/zip'
    format = 'shapefile'
    charset = 'utf-8'
    render_style = 'binary'
    headers = None 

    def render(self, data, media_type=None, renderer_context=None):
        filename = buildFileName(renderer_context.get('request').QUERY_PARAMS.get('fields'), renderer_context.get('request').QUERY_PARAMS.get('iso3'), renderer_context.get('view').fileslug)
        fields = renderer_context.get('request').QUERY_PARAMS.get('fields').split(',')
        createShapefile(data, filename, fields)

        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        archive.write(filename +'.shp', filename +'.shp')
        archive.write(filename +'.shx', filename +'.shx')
        archive.write(filename +'.prj', filename +'.prj')
        archive.write(filename +'.dbf', filename +'.dbf')
        archive.close()
        temp.seek(0)
        return StreamingHttpResponse(temp)

class GeoTIFFRenderer(BaseRenderer):
    media_type = 'image/tiff'
    format = 'geotiff'
    charset = 'utf-8'
    render_style = 'binary'
    headers = None

    def render(self, data, media_type=None, renderer_context=None):
        fileslug = renderer_context.get('view').fileslug
        
        filename_all = buildFileName(renderer_context.get('request').QUERY_PARAMS.get('fields'), renderer_context.get('request').QUERY_PARAMS.get('iso3'), fileslug)
        fields = renderer_context.get('request').QUERY_PARAMS.get('fields').split(',')
        iso3s = renderer_context.get('request').QUERY_PARAMS.get('iso3').split(',')
        
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        print fields
        for field in fields:
            if (field != 'wkb_geometry' and field != 'unit'):
                for iso3 in iso3s:
                    filename = buildFileName(field, iso3, fileslug)
                    f = list()
                    f.append(field)
                    createShapefile(data, filename, f)
                    createGeoTIFF(data, filename, field)
                    archive.write(filename +'.tif', filename +'.tif')
        archive.close()
        temp.seek(0)
        return StreamingHttpResponse(temp)

class ImageRenderer(BaseRenderer):
    media_type = 'image/tiff'
    format = 'geotiff'
    charset = 'utf-8'
    render_style = 'binary'
    headers = None
    # to be continued

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

class YieldViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Yield.objects.all()
    serializer_class = YieldSerializer

    paginate_by = None
    fileslug = 'yield'
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer, ShapefileRenderer, GeoTIFFRenderer, ImageRenderer)
    def get_queryset(self):
        
        queryset = Yield.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

    # set filename
    def finalize_response(self, request, response, *args, **kwargs):
        response = super(YieldViewSet, self).finalize_response(request, response, *args, **kwargs)
        if response.accepted_renderer.format == 'shapefile' or response.accepted_renderer.format == 'geotiff':
            filename = buildFileName(request.QUERY_PARAMS.get('fields'), request.QUERY_PARAMS.get('iso3'), 'yield')
            response['content-disposition'] = 'attachment; filename=' + filename + '.zip'
        return response

class YieldPaginatedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Yield.objects.all()
    serializer_class = YieldSerializer
    paginate_by = 20
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomPaginatedCSVRenderer)

    def get_queryset(self):
        queryset = Yield.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

class AreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    paginate_by = None
    fileslug = 'physical_area'
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer, ShapefileRenderer, GeoTIFFRenderer, ImageRenderer)
    def get_queryset(self):
        
        queryset = Yield.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

    # set filename
    def finalize_response(self, request, response, *args, **kwargs):
        response = super(YieldViewSet, self).finalize_response(request, response, *args, **kwargs)
        if response.accepted_renderer.format == 'shapefile' or response.accepted_renderer.format == 'geotiff':
            filename = buildFileName(request.QUERY_PARAMS.get('fields'), request.QUERY_PARAMS.get('iso3'), 'yield')
            response['content-disposition'] = 'attachment; filename=' + filename + '.zip'
        return response

class AreaPaginatedViewSet(viewsets.ModelViewSet):
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

class ProdViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Prod.objects.all()
    serializer_class = ProdSerializer

    paginate_by = None
    fileslug = 'production'
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer, ShapefileRenderer, GeoTIFFRenderer, ImageRenderer)
    def get_queryset(self):
        
        queryset = Yield.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

    # set filename
    def finalize_response(self, request, response, *args, **kwargs):
        response = super(YieldViewSet, self).finalize_response(request, response, *args, **kwargs)
        if response.accepted_renderer.format == 'shapefile' or response.accepted_renderer.format == 'geotiff':
            filename = buildFileName(request.QUERY_PARAMS.get('fields'), request.QUERY_PARAMS.get('iso3'), 'yield')
            response['content-disposition'] = 'attachment; filename=' + filename + '.zip'
        return response

    
class ProdPaginatedViewSet(viewsets.ModelViewSet):
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

class HarvestedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows yields to be viewed or edited.
    """
    queryset = Harvested.objects.all()
    serializer_class = HarvestedSerializer

    paginate_by = None
    fileslug = 'harvested_area'
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CustomCSVRenderer, ShapefileRenderer, GeoTIFFRenderer, ImageRenderer)
    def get_queryset(self):
        
        queryset = Yield.objects.all()
        iso3 = self.request.QUERY_PARAMS.get('iso3', None)
        if iso3 is not None:
            iso3 = iso3.split(',')
            queryset = queryset.filter(iso3__in=iso3)
        return queryset

    # set filename
    def finalize_response(self, request, response, *args, **kwargs):
        response = super(YieldViewSet, self).finalize_response(request, response, *args, **kwargs)
        if response.accepted_renderer.format == 'shapefile' or response.accepted_renderer.format == 'geotiff':
            filename = buildFileName(request.QUERY_PARAMS.get('fields'), request.QUERY_PARAMS.get('iso3'), 'yield')
            response['content-disposition'] = 'attachment; filename=' + filename + '.zip'
        return response

class HarvestedPaginatedViewSet(viewsets.ModelViewSet):
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

'''class UserViewSet(viewsets.ModelViewSet):
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
