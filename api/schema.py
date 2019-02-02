import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Schemes as SchemesModel
from models import NAVs as NAVModel

class Scheme(MongoengineObjectType):
    class Meta:
        model = SchemesModel
        interfaces = (Node,)

class NAV(MongoengineObjectType):
    class Meta:
        model = NAVModel
        interfaces = (Node,)

class Query(graphene.ObjectType):
    all_schemes = MongoengineConnectionField(Scheme)
    all_navs = MongoengineConnectionField(NAV)

schema = graphene.Schema(query=Query, types=[Scheme, NAV])
