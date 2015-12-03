from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quickstart.models import Area, Yield, Prod, Harvested

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


#class YieldSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Yield
#        fields = ('iso3', 'prod_level', 'alloc_key', 'cell5m', 'rec_type', 'unit', 'whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest', 'whea_i', 'rice_i', 'maiz_i', 'barl_i', 'pmil_i', 'smil_i', 'sorg_i', 'ocer_i', 'pota_i', 'swpo_i', 'yams_i', 'cass_i', 'orts_i', 'bean_i', 'chic_i', 'cowp_i', 'pige_i', 'lent_i', 'opul_i', 'soyb_i', 'grou_i', 'cnut_i', 'oilp_i', 'sunf_i', 'rape_i', 'sesa_i', 'ooil_i', 'sugc_i', 'sugb_i', 'cott_i', 'ofib_i', 'acof_i', 'rcof_i', 'coco_i', 'teas_i', 'toba_i', 'bana_i', 'plnt_i', 'trof_i', 'temf_i', 'vege_i', 'rest_i', 'crea_date', 'year_data', 'source', 'scale_year', 'name_cntr', 'name_adm1', 'whea_h', 'whea_l', 'whea_s', 'rice_h', 'rice_l', 'rice_s', 'maiz_h', 'maiz_l', 'maiz_s', 'barl_h', 'barl_l', 'barl_s', 'pmil_h', 'pmil_l', 'pmil_s', 'smil_h', 'smil_l', 'smil_s', 'sorg_h', 'sorg_l', 'sorg_s', 'ocer_h', 'ocer_l', 'ocer_s', 'pota_h', 'pota_l', 'pota_s', 'swpo_h', 'swpo_l', 'swpo_s', 'yams_h', 'yams_l', 'yams_s', 'cass_h', 'cass_l', 'cass_s', 'orts_h', 'orts_l', 'orts_s', 'bean_h', 'bean_l', 'bean_s', 'chic_h', 'chic_l', 'chic_s', 'cowp_h', 'cowp_l', 'cowp_s', 'pige_h', 'pige_l', 'pige_s', 'lent_h', 'lent_l', 'lent_s', 'opul_h', 'opul_l', 'opul_s', 'soyb_h', 'soyb_l', 'soyb_s', 'grou_h', 'grou_l', 'grou_s', 'cnut_h', 'cnut_l', 'cnut_s', 'oilp_h', 'oilp_l', 'oilp_s', 'sunf_h', 'sunf_l', 'sunf_s', 'rape_h', 'rape_l', 'rape_s', 'sesa_h', 'sesa_l', 'sesa_s', 'ooil_h', 'ooil_l', 'ooil_s', 'sugc_h', 'sugc_l', 'sugc_s', 'sugb_h', 'sugb_l', 'sugb_s', 'cott_h', 'cott_l', 'cott_s', 'ofib_h', 'ofib_l', 'ofib_s', 'acof_h', 'acof_l', 'acof_s', 'rcof_h', 'rcof_l', 'rcof_s', 'coco_h', 'coco_l', 'coco_s', 'teas_h', 'teas_l', 'teas_s', 'toba_h', 'toba_l', 'toba_s', 'bana_h', 'bana_l', 'bana_s', 'plnt_h', 'plnt_l', 'plnt_s', 'trof_h', 'trof_l', 'trof_s', 'temf_h', 'temf_l', 'temf_s', 'vege_h', 'vege_l', 'vege_s', 'rest_h', 'rest_l', 'rest_s', 'x', 'y', 'hc_seq5m')

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].QUERY_PARAMS.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            mandatory = set([u'iso3', u'cell5m', u'unit', u'alloc_key', u'wkb_geometry', u'prod_level', u'crea_date', u'name_cntr', u'name_adm1', u'name_adm2'])
            existing = set(self.fields.keys())
            for field_name in existing - allowed - mandatory:
                self.fields.pop(field_name)

class AreaSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        fields = ('wkb_geometry','iso3', 'cell5m', 'alloc_key', 'unit', 'whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest', 'whea_i', 'rice_i', 'maiz_i', 'barl_i', 'pmil_i', 'smil_i', 'sorg_i', 'ocer_i', 'pota_i', 'swpo_i', 'yams_i', 'cass_i', 'orts_i', 'bean_i', 'chic_i', 'cowp_i', 'pige_i', 'lent_i', 'opul_i', 'soyb_i', 'grou_i', 'cnut_i', 'oilp_i', 'sunf_i', 'rape_i', 'sesa_i', 'ooil_i', 'sugc_i', 'sugb_i', 'cott_i', 'ofib_i', 'acof_i', 'rcof_i', 'coco_i', 'teas_i', 'toba_i', 'bana_i', 'plnt_i', 'trof_i', 'temf_i', 'vege_i', 'rest_i', 'crea_date', 'year_data', 'source', 'scale_year', 'name_cntr', 'name_adm1', 'whea_r', 'rice_r', 'maiz_r', 'barl_r', 'pmil_r', 'smil_r', 'sorg_r', 'ocer_r', 'pota_r', 'swpo_r', 'yams_r', 'cass_r', 'orts_r', 'bean_r', 'chic_r', 'cowp_r', 'pige_r', 'lent_r', 'opul_r', 'soyb_r', 'grou_r', 'cnut_r', 'oilp_r', 'sunf_r', 'rape_r', 'sesa_r', 'ooil_r', 'sugc_r', 'sugb_r', 'cott_r', 'ofib_r', 'acof_r', 'rcof_r', 'coco_r', 'teas_r', 'toba_r', 'bana_r', 'plnt_r', 'trof_r', 'temf_r', 'vege_r', 'rest_r', 'prod_level', 'crea_date', 'name_cntr', 'name_adm1', 'name_adm2')

class YieldSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Yield
        fields = ('wkb_geometry','iso3', 'cell5m', 'alloc_key', 'unit', 'whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest', 'whea_i', 'rice_i', 'maiz_i', 'barl_i', 'pmil_i', 'smil_i', 'sorg_i', 'ocer_i', 'pota_i', 'swpo_i', 'yams_i', 'cass_i', 'orts_i', 'bean_i', 'chic_i', 'cowp_i', 'pige_i', 'lent_i', 'opul_i', 'soyb_i', 'grou_i', 'cnut_i', 'oilp_i', 'sunf_i', 'rape_i', 'sesa_i', 'ooil_i', 'sugc_i', 'sugb_i', 'cott_i', 'ofib_i', 'acof_i', 'rcof_i', 'coco_i', 'teas_i', 'toba_i', 'bana_i', 'plnt_i', 'trof_i', 'temf_i', 'vege_i', 'rest_i', 'crea_date', 'year_data', 'source', 'scale_year', 'name_cntr', 'name_adm1', 'whea_r', 'rice_r', 'maiz_r', 'barl_r', 'pmil_r', 'smil_r', 'sorg_r', 'ocer_r', 'pota_r', 'swpo_r', 'yams_r', 'cass_r', 'orts_r', 'bean_r', 'chic_r', 'cowp_r', 'pige_r', 'lent_r', 'opul_r', 'soyb_r', 'grou_r', 'cnut_r', 'oilp_r', 'sunf_r', 'rape_r', 'sesa_r', 'ooil_r', 'sugc_r', 'sugb_r', 'cott_r', 'ofib_r', 'acof_r', 'rcof_r', 'coco_r', 'teas_r', 'toba_r', 'bana_r', 'plnt_r', 'trof_r', 'temf_r', 'vege_r', 'rest_r', 'prod_level', 'crea_date', 'name_cntr', 'name_adm1', 'name_adm2')

class ProdSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prod
        fields = ('wkb_geometry','iso3', 'cell5m', 'alloc_key', 'unit', 'whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest', 'whea_i', 'rice_i', 'maiz_i', 'barl_i', 'pmil_i', 'smil_i', 'sorg_i', 'ocer_i', 'pota_i', 'swpo_i', 'yams_i', 'cass_i', 'orts_i', 'bean_i', 'chic_i', 'cowp_i', 'pige_i', 'lent_i', 'opul_i', 'soyb_i', 'grou_i', 'cnut_i', 'oilp_i', 'sunf_i', 'rape_i', 'sesa_i', 'ooil_i', 'sugc_i', 'sugb_i', 'cott_i', 'ofib_i', 'acof_i', 'rcof_i', 'coco_i', 'teas_i', 'toba_i', 'bana_i', 'plnt_i', 'trof_i', 'temf_i', 'vege_i', 'rest_i', 'crea_date', 'year_data', 'source', 'scale_year', 'name_cntr', 'name_adm1', 'whea_r', 'rice_r', 'maiz_r', 'barl_r', 'pmil_r', 'smil_r', 'sorg_r', 'ocer_r', 'pota_r', 'swpo_r', 'yams_r', 'cass_r', 'orts_r', 'bean_r', 'chic_r', 'cowp_r', 'pige_r', 'lent_r', 'opul_r', 'soyb_r', 'grou_r', 'cnut_r', 'oilp_r', 'sunf_r', 'rape_r', 'sesa_r', 'ooil_r', 'sugc_r', 'sugb_r', 'cott_r', 'ofib_r', 'acof_r', 'rcof_r', 'coco_r', 'teas_r', 'toba_r', 'bana_r', 'plnt_r', 'trof_r', 'temf_r', 'vege_r', 'rest_r', 'prod_level', 'crea_date', 'name_cntr', 'name_adm1', 'name_adm2')

class HarvestedSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Harvested
        fields = ('wkb_geometry','iso3', 'cell5m', 'alloc_key', 'unit', 'whea', 'rice', 'maiz', 'barl', 'pmil', 'smil', 'sorg', 'ocer', 'pota', 'swpo', 'yams', 'cass', 'orts', 'bean', 'chic', 'cowp', 'pige', 'lent', 'opul', 'soyb', 'grou', 'cnut', 'oilp', 'sunf', 'rape', 'sesa', 'ooil', 'sugc', 'sugb', 'cott', 'ofib', 'acof', 'rcof', 'coco', 'teas', 'toba', 'bana', 'plnt', 'trof', 'temf', 'vege', 'rest', 'whea_i', 'rice_i', 'maiz_i', 'barl_i', 'pmil_i', 'smil_i', 'sorg_i', 'ocer_i', 'pota_i', 'swpo_i', 'yams_i', 'cass_i', 'orts_i', 'bean_i', 'chic_i', 'cowp_i', 'pige_i', 'lent_i', 'opul_i', 'soyb_i', 'grou_i', 'cnut_i', 'oilp_i', 'sunf_i', 'rape_i', 'sesa_i', 'ooil_i', 'sugc_i', 'sugb_i', 'cott_i', 'ofib_i', 'acof_i', 'rcof_i', 'coco_i', 'teas_i', 'toba_i', 'bana_i', 'plnt_i', 'trof_i', 'temf_i', 'vege_i', 'rest_i', 'crea_date', 'year_data', 'source', 'scale_year', 'name_cntr', 'name_adm1', 'whea_r', 'rice_r', 'maiz_r', 'barl_r', 'pmil_r', 'smil_r', 'sorg_r', 'ocer_r', 'pota_r', 'swpo_r', 'yams_r', 'cass_r', 'orts_r', 'bean_r', 'chic_r', 'cowp_r', 'pige_r', 'lent_r', 'opul_r', 'soyb_r', 'grou_r', 'cnut_r', 'oilp_r', 'sunf_r', 'rape_r', 'sesa_r', 'ooil_r', 'sugc_r', 'sugb_r', 'cott_r', 'ofib_r', 'acof_r', 'rcof_r', 'coco_r', 'teas_r', 'toba_r', 'bana_r', 'plnt_r', 'trof_r', 'temf_r', 'vege_r', 'rest_r', 'prod_level', 'crea_date', 'name_cntr', 'name_adm1', 'name_adm2')
