import graphene
import graph_api.orders.schema


class Query(graph_api.orders.schema.Query, graphene.ObjectType):
    pass


class Mutation(graph_api.orders.schema.Mutation, graphene.ObjectType):
    pass
