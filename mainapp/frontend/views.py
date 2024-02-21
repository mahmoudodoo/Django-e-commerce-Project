from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Item, OrderItem, Order, BillingAddress, Coupon, Payment
from django.views.generic import View, DetailView, ListView
from .forms import ShippingAddressForm,CouponForm

# Create your views here.
class HomeView(ListView):
 model = Item
 paginate_by = 6
 template_name= "home.html"

class DetailView(DetailView):
  model= Item
  template_name= "detail.html"



@login_required(login_url='../accounts/login/')
def add_to_cart(request, slug):
   item = get_object_or_404(Item, slug=slug)
   order_item, created = OrderItem.objects.get_or_create(
       item=item,
       user=request.user,
       ordered=False
   )


   order_q = Order.objects.filter(user=request.user, ordered=False)


   if order_q.exists():
       order = order_q[0]


       if order.items.filter(item__slug=item.slug).exists():
           order_item.quantity += 1
           order_item.save()
           messages.info(request, "Item added to your cart")
           return redirect("frontend:summary")
       else:
           messages.info(request, "Item added to your cart")
           order.items.add(order_item)
           return redirect("frontend:summary")


   else:
       ordered_date = timezone.now()
       order = Order.objects.create(user=request.user, ordered_date=ordered_date)
       order.items.add(order_item)
       messages.info(request, "Item added to your cart")
       return redirect("frontend:summary")
   

class OrderSummaryView(LoginRequiredMixin, View):
  def get(self, *args, **kwargs):
    try:
        current_order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'object': current_order
        }
        return render(self.request, 'summary.html', context)
    except ObjectDoesNotExist:
        messages.warning(self.request, "You do not have an active order")
        return redirect('/')
    


@login_required(login_url='../accounts/login/')
def remove_single_item(request, slug):
   item = get_object_or_404(Item, slug=slug)


   order_q = Order.objects.filter(user=request.user, ordered=False)


   if order_q.exists():
       order = order_q[0]


       if order.items.filter(item__slug=item.slug).exists():
           order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]


           if order_item.quantity > 1:
               order_item.quantity -= 1
               order_item.save()
           else:
               order.items.remove(order_item)


           messages.info(request, "Cart updated")
           return redirect("frontend:summary")
       else:
           messages.info(request, "Item was not in your cart")
           return redirect("frontend:detail", slug=slug)


   else:
       messages.info(request, "You do not have an active order")
       return redirect("fronted:detail", slug=slug)
   

class ShippingAddressView(View):
   def get(self, *args, **kwargs):
       try:
           order = Order.objects.get(user=self.request.user, ordered=False)
           form = ShippingAddressForm()
           context = {
               'form': form,
               'order': order,
               'couponform': CouponForm(),
               'display_coupon_form': True
           }
           return render(self.request, 'shipping-address.html', context)
       except ObjectDoesNotExist:
           messages.info(self.request, 'You do not have an active order')
           return redirect('frontend:shipping-address')


   def post(self, *args, **kwargs):
       form = ShippingAddressForm(self.request.POST or None)
       try:
           order = Order.objects.get(user=self.request.user, ordered=False)
           if form.is_valid():
               street_address = form.cleaned_data.get('street_address')
               apartment_address = form.cleaned_data.get('apartment_address')
               zip_code = form.cleaned_data.get('zip_code')


               billing_address = BillingAddress(
                   user=self.request.user,
                   street_address=street_address,
                   apartment=apartment_address,
                   zip=zip_code
               )


               billing_address.save()
               order.billing_address = billing_address
               order.save()


               messages.info(self.request, "Address added to order")
               return redirect('frontend:payment')
       except ObjectDoesNotExist:
           messages.info(self.request, "No active order")
           return redirect('frontend:summary')
       

def get_coupon(request, code):
   try:
       coupon = Coupon.objects.get(code=code)
       return coupon
   except ObjectDoesNotExist:
       messages.info(request, "This coupon is not valid")
       return redirect('frontend:shipping-address')




class addCouponView(View):
   def post(self, *args, **kwargs):
       form = CouponForm(self.request.POST or None)
       if form.is_valid():
           try:
               code = form.cleaned_data.get('code')
               order = Order.objects.get(user=self.request.user, ordered=False)
               order.coupon = get_coupon(self.request, code)
               order.save()
               messages.success(self.request, "Coupon added")
               return redirect('frontend:shipping-address')
           except ObjectDoesNotExist:
               messages.success(self.request, "You do not have an active order")
               return redirect('frontend:shipping-address')
           

