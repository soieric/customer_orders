import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Order
import africastalking

# Initialize Africa's Talking
africastalking.initialize(username="sandbox", api_key="atsk_0f086f0ee29b6b7aeef81d11616f8791fe6b948e61cc55a8f6b8ceeed31e88744508a04d")
sms = africastalking.SMS

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "code")

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "item", "amount", "time")

class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)

    class Arguments:
        name = graphene.String(required=True)
        code = graphene.String(required=True)

    def mutate(self, info, name, code):
        customer = Customer.objects.create(name=name, code=code)
        return CreateCustomer(customer=customer)

class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        customer_id = graphene.Int(required=True)
        item = graphene.String(required=True)
        amount = graphene.Float(required=True)

    def mutate(self, info, customer_id, item, amount):
        customer = Customer.objects.get(id=customer_id)
        order = Order.objects.create(customer=customer, item=item, amount=amount)

        # Send SMS via Africa's Talking
        message = f"Hello {customer.name}, your order '{item}' has been placed successfully."
        try:
            sms.send(message, ["+254712962787"])  
        except Exception as e:
            print(f"Error sending SMS: {e}")

        return CreateOrder(order=order)

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    orders = graphene.List(OrderType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    create_order = CreateOrder.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
