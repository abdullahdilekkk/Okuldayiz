from django_filters import rest_framework
from .models import School

class SchoolFilter(rest_framework.FilterSet):
    min_price = rest_framework.NumberFilter(field_name="min_price", lookup_expr="gte")
    max_price = rest_framework.NumberFilter(field_name="max_price", lookup_expr="lte")
    features = rest_framework.CharFilter(method='filter_features')

    class Meta:
        model = School
        fields = ['city', 'district', 'school_type', 'min_price', 'max_price']

    def filter_features(self, queryset, name, value):
        # features=1,2,3 şeklinde geldiğinde virgülle ayırıp çoklu filtreleme yapar
        features_ids = value.split(',')
        if features_ids:
            return queryset.filter(features__id__in=features_ids).distinct()
        return queryset
