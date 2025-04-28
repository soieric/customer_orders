import core.schema
import graphene

class Query(core.schema.Query, graphene.ObjectType):
    pass

class Mutation(core.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
