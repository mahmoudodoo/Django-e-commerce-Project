from django.contrib import admin
from .models import Item, Order, OrderItem, Coupon, Payment, BillingAddress, Refund


admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(Refund)