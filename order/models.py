from django.db import models
from order.enums import OrderStatus
from order.querysets import OrderQuerySet


class Order(models.Model):
    customer = models.ForeignKey('user_management.Customer', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default=OrderStatus.PENDING, choices=OrderStatus.choices)
    total_price = models.FloatField(default=0)
    
    objects = OrderQuerySet.as_manager()

    def calculate_total_price(self):
        orderItems = self.orderitem_set.all()
        price = 0
        for orderItem in orderItems:
            temp = orderItem.product.price * orderItem.quantity
            price += temp
            price = round(price, 2)
        return price

    def accept(self):
        self.status = OrderStatus.ACCEPTED
        self.save()

    def reject(self):
        self.status = OrderStatus.REJECTED
        self.save()

    def deliver(self):
        self.status = OrderStatus.DELIVERED
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELLED
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order.customer.user.username} - {self.product.name}'

    def save(self, *args, **kwargs):
        """You can not modify this method"""
        super().save(*args, **kwargs)
        self.order.total_price = self.order.calculate_total_price()
        self.order.save()
