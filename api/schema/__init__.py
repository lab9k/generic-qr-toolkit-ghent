from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.rest_framework.mutation import SerializerMutation
import graphene
import logging

from api import models, serializers
from api.schema.department import DepartmentQueries, DepartmentMutations

logger = logging.getLogger(__file__)


# class CreateDepartmentMutation(graphene.Mutation):
#     department = graphene.Field(DepartmentType)
#     message = graphene.String()
#     status = graphene.Int()
#
#     class Arguments:
#         name = graphene.String(required=True)
#
#     @classmethod
#     def mutate(cls, root, info, **kwargs):
#         serializer = serializers.DepartmentSerializer(data=kwargs)
#         if serializer.is_valid():
#             obj = serializer.save()
#             msg = 'success'
#             status = 201
#         else:
#             msg = serializer.errors
#             obj = None
#             logger.error(msg=msg)
#         return cls(department=obj, message=msg, status=201)


class QrCodeType(DjangoObjectType):
    class Meta:
        model = models.QRCode


class ApiHitType(DjangoObjectType):
    class Meta:
        model = models.ApiHit


class LinkUrlType(DjangoObjectType):
    class Meta:
        model = models.LinkUrl


class Query(DepartmentQueries, graphene.ObjectType):
    qrcodes = DjangoListField(QrCodeType)

    apihits = DjangoListField(ApiHitType)


class Mutations(DepartmentMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations, types=[LinkUrlType, ])
