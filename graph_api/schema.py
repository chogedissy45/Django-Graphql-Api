import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graph_api.orders.models import Order, Customer
import africastalking

username = "sandbox"
api_key = "0b092c6c17a1499e1a93d5a8e864194c454ada5181f7aa14d3295d3101a0cb02"


sms = africastalking.SMSService(username, api_key)

# async callback
def onFinish(err, res):
    if err is not None:
        raise err
    print(res)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer


class Query(ObjectType):
    customer = graphene.Field(CustomerType, id=graphene.Int())
    order = graphene.Field(OrderType, id=graphene.Int())
    customers = graphene.List(CustomerType)
    orders = graphene.List(OrderType)

    def resolve_customer(self, info, **kwargs):
        id = kwargs.get("id")

        if id is not None:
            return Customer.objects(pk=id)
        return None

    def resolve_order(self, info, **kwargs):
        id = kwargs.get("id")
        if id is not None:
            return Order.objects.get(pk=id)

        return None

    def resolve_customers(self, info, **kwargs):
        return Customer.objects.all()

    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()


class OrderInput(graphene.InputObjectType):
    id = graphene.ID()
    item = graphene.String()
    amount = graphene.Int()
    time = graphene.Int()


class CustomerInput(graphene.InputObjectType):
    code = graphene.Int()
    name = graphene.String()
    orders = graphene.List(OrderInput)


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    ok = graphene.Boolean()
    order = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        order_instance = Order(item=input.item, amount=input.amount, time=input.time)
        order_instance.save()
        return CreateOrder(ok=ok, order=order_instance)


class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    ok = graphene.Boolean()
    customer = graphene.Field(CustomerType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        orders = []
        for order_input in input.orders:
            order = Order.objects.get(pk=order_input.id)
            if order is None:
                return CreateCustomer(ok=False, customer=None)
            orders.append(order)
        customer_instance = Customer(name=input.name, code=input.code)
        print(orders)
        customer_instance.save()
        # TODO: Send message
        sms.send(
            "Your order has been approved", ["+254" + str(input.code)], callback=onFinish
        )
        return CreateCustomer(ok=ok, customer=customer_instance)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
