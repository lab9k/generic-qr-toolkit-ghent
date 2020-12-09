import graphene
from graphene_django import DjangoObjectType, DjangoListField

from api.models import Department
from api.serializers import DepartmentSerializer


class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department


class CreateDepartmentMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    department = graphene.Field(DepartmentType)
    errors = graphene.String(required=False)
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, name):
        serializer = DepartmentSerializer(data=dict(name=name))
        if serializer.is_valid():
            dep = serializer.save()
            ok = True
            errors = None
        else:
            ok = False
            dep = None
            errors = ', '.join(serializer.errors['name'])
        return cls(department=dep, ok=ok, errors=errors)


class UpdateDepartmentMutation(graphene.Mutation):
    # Input arguments
    class Arguments:
        pk = graphene.ID(required=True)
        name = graphene.String(required=True)

    # class fields define response of mutation
    department = graphene.Field(DepartmentType)
    errors = graphene.String(required=False)
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, pk, name):
        try:
            dep = Department.objects.get(pk=pk)
            dep.name = name
            dep.save()
            errors = None
            ok = True
        except Department.DoesNotExist:
            errors = f'The department with pk={pk} does not exist.'
            ok = False
            dep = None
        return cls(department=dep, errors=errors, ok=ok)


class DeleteDepartmentMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.ID()

    errors = graphene.String(required=False)
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, pk):
        try:
            obj = Department.objects.get(pk=pk)
            obj.delete()
            errors = None
            ok = True
        except Department.DoesNotExist:
            errors = f'The department with pk={pk} does not exist.'
            ok = False
        return cls(errors=errors, ok=ok)


class DepartmentQueries(graphene.ObjectType):
    departments = DjangoListField(DepartmentType)
    department = graphene.Field(DepartmentType, id=graphene.ID(required=False), name=graphene.String(required=False))

    def resolve_department(self, info, id=None, name=None):
        if id is not None and name is not None:
            return Department.objects.get(id=id, name=name)
        if id is not None:
            return Department.objects.get(id=id)
        if name is not None:
            return Department.objects.get(name=name)
        return None


class DepartmentMutations(graphene.ObjectType):
    create_department = CreateDepartmentMutation.Field()
    update_department = UpdateDepartmentMutation.Field()
    delete_department = DeleteDepartmentMutation.Field()
