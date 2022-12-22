from django.views.generic import TemplateView, CreateView, DeleteView
from .models import Product, Category, Cart, CartDetails, OrderDetails, Orders, Status
from django.forms.models import model_to_dict
from django.http import JsonResponse


class BaseView(TemplateView):

    def get_context_data(self, **kwargs):
        self.request.session[0] = 'barr'
        sessionid = self.request.COOKIES.get('sessionid')

        context = super().get_context_data(**kwargs)

        try:
            carts = CartDetails.objects.filter(cart_id=Cart.objects.get_or_create(guest_session_id=sessionid)[0].id)
            total = 0
            for cart in carts:
                total += cart.count * cart.product.price
            context['total'] = total
            context['carts'] = carts
        except:
            print('error')

        return context


class IndexView(BaseView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.objects.all()[:6]
        return context


class CartView(BaseView):
    template_name = 'cart.html'


class CheckoutView(BaseView):
    template_name = 'checkout.html'


class ShopView(BaseView):
    template_name = 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            category = self.request.GET['cat']
        except:
            category = 0

        try:
            brand = self.request.GET['brand']
        except:
            brand = 0

        if category != 0:
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()

        if brand != 0:
            products = products.filter(brand=brand)
        context['products'] = products
        context['categories'] = Category.objects.all()
        context['activeCategory'] = category
        return context


class ProductDetailsView(BaseView):
    template_name = 'product-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        try:
            id = self.request.GET['id']
        except:
            id = 1

        context['product'] = Product.objects.filter(id=id)[0]

        return context


class ProductCreate(CreateView):
    model = Cart
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        id = self.request.POST['id']
        count = self.request.POST['count']
        sessionid = self.request.COOKIES.get('sessionid')

        product = Product.objects.filter(id=id)[0]
        cart, created = Cart.objects.get_or_create(guest_session_id=sessionid)
        cart.save()
        current_cart, created = CartDetails.objects.get_or_create(cart_id=cart, product=product,
                                                                  defaults={'count': 0})
        current_cart.count += int(count)
        current_cart.save()
        print(product)
        carts = CartDetails.objects.filter(cart_id=cart)

        new_carts = [{'product': dict(map(lambda kv: (kv[0], str(kv[1])), model_to_dict(cart.product).items())),
                      'count': str(cart.count)} for cart in carts]

        return JsonResponse(
            {'ok': 'ok', 'length': len(new_carts)}, safe=False)


class ProductDelete(DeleteView):
    model = Cart
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        id = self.request.POST['id']
        sessionid = self.request.COOKIES.get('sessionid')
        cart_id = Cart.objects.filter(guest_session_id=sessionid)[0]

        product = CartDetails.objects.get(product_id=id)
        product.delete()
        carts = CartDetails.objects.filter(cart_id=cart_id)

        new_carts = [{'product': dict(map(lambda kv: (kv[0], str(kv[1])), model_to_dict(cart.product).items())),
                      'count': str(cart.count)} for cart in carts]
        print(product)
        carts = CartDetails.objects.filter(cart_id=Cart.objects.filter(guest_session_id=sessionid)[0].id)
        total = 0
        for cart in carts:
            total += cart.count * cart.product.price
        return JsonResponse({'total': total, 'length': len(new_carts)})


class ChangeProductCount(CreateView):
    def post(self, request, *args, **kwargs):
        id = self.request.POST['id']
        count = self.request.POST['count']
        sessionid = self.request.COOKIES.get('sessionid')
        cart, created = Cart.objects.get_or_create(guest_session_id=sessionid)
        current_cart = CartDetails.objects.get(cart_id=cart, product_id=id)
        current_cart.count = count
        current_cart.save()

        carts = CartDetails.objects.filter(cart_id=Cart.objects.get_or_create(guest_session_id=sessionid)[0].id)
        total = 0
        for cart in carts:
            total += cart.count * cart.product.price
        return JsonResponse(
            {'total': str(total)}, safe=False)


class OrderCreate(CreateView):
    success_url = 'checkout'

    def post(self, request, *args, **kwargs):
        sessionid = self.request.COOKIES.get('sessionid')

        fname = self.request.POST['fname']
        lname = self.request.POST['lname']
        addr = self.request.POST['addr']
        mail = self.request.POST['mail']
        zip = self.request.POST['zip']
        try:
            comment = self.request.POST['comment']
        except:
            comment = ''
        total = self.request.POST['total']
        try:
            current_order = Orders(guest_session_id=sessionid, address=addr, mail=mail, fname=fname,
                                   lname=lname, status=Status.objects.get(id=1), zip=zip, comment=comment,
                                   total_sum=float(total))
            current_order.save()
            cart_id = Cart.objects.filter(guest_session_id=sessionid)[0]
            carts = CartDetails.objects.filter(cart_id=cart_id)
            for cart in carts:
                order_detail, created = OrderDetails.objects.get_or_create(order_id=current_order, product=cart.product,
                                                                           count=cart.count)
                order_detail.save()

            cart_id.delete()

        except:
            print('error')
        return JsonResponse({'ok': 'ok'})
