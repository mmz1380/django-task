from django.db.models import *

class CustomerQuerySet(QuerySet):
    def annotate_with_total_spending(self):
        return self.annotate(total_spending=Sum(F'order__total_price')).values()

    def annotate_with_order_count(self):
        return self.annotate(order_count=Count(F'order__total_price')).values()