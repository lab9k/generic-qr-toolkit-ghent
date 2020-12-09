import graphene
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from django_filters import FilterSet, DateTimeFilter

from api.models import ApiHit


class ApiHitFilter(FilterSet):
    hit_date = DateTimeFilter(field_name='hit_date', lookup_expr='gt')

    class Meta:
        model = ApiHit
        fields = ['hit_date', ]


class ApiHitType(DjangoObjectType):
    class Meta:
        model = ApiHit
        filterset_class = ApiHitFilter
        interfaces = (relay.Node,)


class ApiHitQueries(graphene.ObjectType):
    apihits = DjangoFilterConnectionField(ApiHitType)
