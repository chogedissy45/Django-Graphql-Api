from django.db import models


class Order(models.Model):
    item = models.CharField(max_length=100)
    amount = models.IntegerField()
    time = models.IntegerField()

    def __str__(self):
        return self.item

    class Meta:
        ordering = ('item',)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField()
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
