from django.db.models import QuerySet
from django.db.models import Sum
from datetime import *


class OrderQuerySet(QuerySet):
    def by_customer(self, customer):
        return self.filter(customer__exact=customer)

    def total_price(self):
        return self.aggregate(Sum("total_price")).get("total_price__sum")

    def total_price_by_customer(self, customer):
        return self.by_customer(customer).aggregate(Sum("total_price")).get("total_price__sum")

    def submitted_in_date(self, date_value):
        return self.filter(date__date=date_value)
