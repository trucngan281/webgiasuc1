
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F, Case, When, Value, PositiveSmallIntegerField
from shop.models import Order, OrderDetail, Product
from django.contrib import messages

from .forms import CustomerForm
# Create your views here.


def cart_page(request):
    try:
        cart = Order.objects.get(user=request.user, ordered=False)
    except:
        messages.error(request, "You haven't shop yet")
        return render(request, 'base/errors.html')
    context = {
        "cart": cart
    }
    try:
        lineOrder = cart.lineOrder.all()
        context["lineOrderList"] = lineOrder

    except Exception as err:
        print(err)
        context["lineOrderList"] = []

    return render(request, 'cart/cart.html', context)


def checkout(request):

    cart = Order.objects.get(user=request.user, ordered=False)
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer_instance = form.save()
            cart.customer = customer_instance
            cart.ordered = True
            cart.save()
            for order_detail in cart.lineOrder.all():
                order_detail.ordered = True
                order_detail.minus_inventory()
                order_detail.save()
            messages.success(
                request, "Đơn hàng của bạn đã được ghi nhận, chúng tôi sẽ liên lạc với bạn để xác nhận đơn hàng")
            return render(request, 'base/success.html')

    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'cart/checkout.html', context)


def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = OrderDetail.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #print(order.lineOrder.all())
        if order.lineOrder.filter(item__pk=item.pk).exists():
            if order_item.is_available():
                order_item.quantity += 1
                order_item.save()

        else:
            if order_item.is_available():
                order.lineOrder.add(order_item)

    else:
        order = Order.objects.create(
            user=request.user)
        if order_item.is_available():
            order.lineOrder.add(order_item)
    print({'count': order.lineOrder.count(),
          pk: item.get_current_quantity(request.user)})
    return JsonResponse({'count': order.lineOrder.count(), pk: item.get_current_quantity(request.user)})


def minus_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.lineOrder.filter(item__pk=item.pk).exists():
            order_item = OrderDetail.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            return JsonResponse({'count': order.lineOrder.count(), pk: item.get_current_quantity(request.user)})

        else:
            return JsonResponse({'count': order.lineOrder.count(), pk: item.get_current_quantity(request.user)})

    else:
        # messages.info(request, "You do not have an Order")
        return JsonResponse({'count': order.lineOrder.count(), pk: item.get_current_quantity(request.user)})


def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.lineOrder.filter(item__pk=item.pk).exists():
            order_item = OrderDetail.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            return redirect("shop")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("shop", pk=pk)
    else:
        # add message doesnt have order
        messages.info(request, "Bạn chưa có đơn hàng nào")
        return redirect("shop", pk=pk)
