from graphene_django import DjangoObjectType, DjangoListField
import graphene
import logging

from api import models, serializers
from api.schema.department import DepartmentQueries, DepartmentMutations
from api.schema.apihit import ApiHitQueries

logger = logging.getLogger(__file__)


class QrCodeType(DjangoObjectType):
    class Meta:
        model = models.QRCode


class LinkUrlType(DjangoObjectType):
    class Meta:
        model = models.LinkUrl


class Query(DepartmentQueries, ApiHitQueries, graphene.ObjectType):
    qrcodes = DjangoListField(QrCodeType)


class Mutations(DepartmentMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations, types=[LinkUrlType, ])
