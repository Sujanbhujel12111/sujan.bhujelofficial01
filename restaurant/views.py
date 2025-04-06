from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Table, Category, MenuItem, Order, OrderItem, Payment, OrderHistory
from .forms import MenuItemForm, CategoryForm, OrderForm, OrderItemForm, PaymentForm
import json
from django.db.models import Sum
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from .models import Table, MenuItem, OrderItem
from .forms import OrderForm, OrderItemForm
from django.db import models
from django.contrib.auth import views as auth_views
import qrcode
from io import BytesIO


class LoginView(auth_views.LoginView):
    template_name = 'home/login.html'

class LogoutView(auth_views.LogoutView):
    template_name = 'home/logout.html'


@login_required
def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'restaurant/menu.html', {'menu_items': menu_items})

@login_required
def public_menu_view(request):
    menu_items = MenuItem.objects.filter(is_available=True)
    return render(request, 'restaurant/public_menu.html', {'menu_items': menu_items})

@login_required
def generate_qr_code(request):
    menu_url = request.build_absolute_uri(reverse('restaurant:public_menu_view'))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return HttpResponse(buffer, content_type="image/png")

@login_required
def dashboard_view(request):
    today = date.today()
    context = {
        'today_sales': Order.objects.filter(
            created_at__date=today,
            status='completed'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }
    return render(request, 'home/dashboard.html', context)

@login_required
def kitchen_view(request):
    orders = Order.objects.filter(status='preparing')  # Filter orders by "preparing" status
    return render(request, 'restaurant/kitchen.html', {'orders': orders})

@login_required
def place_order(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1)
    menu_items = MenuItem.objects.filter(is_available=True)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, queryset=OrderItem.objects.none())

        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.table = table
            order.status = 'pending'
            total_amount = 0

            # First save the order
            order.save()

            # Then save order items and calculate total
            for form in formset:
                if form.cleaned_data:  # Check if form has data
                    order_item = form.save(commit=False)
                    menu_item = MenuItem.objects.get(id=order_item.item.id)
                    order_item.price = menu_item.price
                    order_item.order = order
                    order_item.save()
                    
                    # Calculate item total and add to order total
                    item_total = order_item.price * order_item.quantity
                    total_amount += item_total

            # Update order with calculated total
            order.total_amount = total_amount
            order.save()

            return redirect('restaurant:order_list')

    else:
        order_form = OrderForm()
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    return render(request, 'restaurant/place_order.html', {
        'table': table,
        'order_form': order_form,
        'formset': formset,
        'menu_items': menu_items,
    })


@login_required
def place_order_takeaway(request):
    OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1)
    menu_items = MenuItem.objects.filter(is_available=True)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, queryset=OrderItem.objects.none())

        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.order_type = 'takeaway'
            order.status = 'pending'
            order.save()

            total_amount = 0  # Initialize total_amount

            # Then save order items and calculate total
            for form in formset:
                if form.cleaned_data:  # Check if form has data
                    order_item = form.save(commit=False)
                    menu_item = MenuItem.objects.get(id=order_item.item.id)
                    order_item.price = menu_item.price
                    order_item.order = order
                    order_item.save()
                    
                    # Calculate item total and add to order total
                    item_total = order_item.price * order_item.quantity
                    total_amount += item_total

            # Update order with calculated total
            order.total_amount = total_amount
            order.save()

            return redirect('restaurant:order_list')

    else:
        order_form = OrderForm()
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    return render(request, 'restaurant/place_order_takeaway.html', {
        'order_form': order_form,
        'formset': formset,
        'menu_items': menu_items,
    })

@login_required
def place_order_delivery(request):
    OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1)
    menu_items = MenuItem.objects.filter(is_available=True)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST, queryset=OrderItem.objects.none())
        delivery_charge = int(request.POST.get('delivery_charge', 100))  # Get delivery charge from form

        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.order_type = 'delivery'
            order.status = 'pending'
            order.delivery_charge = delivery_charge  # Save delivery charge
            order.save()

            total_amount = 0

            for form in formset:
                if form.cleaned_data:
                    order_item = form.save(commit=False)
                    menu_item = MenuItem.objects.get(id=order_item.item.id)
                    order_item.price = menu_item.price
                    order_item.order = order
                    order_item.save()
                    
                    item_total = order_item.price * order_item.quantity
                    total_amount += item_total

            # Save the base total amount (without delivery charge)
            order.total_amount = total_amount
            order.save()

            return redirect('restaurant:order_list')

    else:
        order_form = OrderForm()
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    return render(request, 'restaurant/place_order_delivery.html', {
        'order_form': order_form,
        'formset': formset,
        'menu_items': menu_items,
    })

@login_required
def close_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'completed'
        order.payment_status = 'paid'  # Assuming payment is settled here
        order.save()
        order.move_to_history()
        return redirect('restaurant:order_list')
    return render(request, 'restaurant/close_order.html', {'order': order})


@login_required
def payment_success(request):
    return render(request, 'restaurant/payment_success.html')

@login_required
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.ORDER_STATUS_CHOICES):
            order.status = status
            order.save()
    return redirect('restaurant:order_details', order_id=order.order_id)

@login_required
def process_payment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.edited_by = request.user
            payment.save()
            return redirect('restaurant:order_details', order_id=order.order_id)
    else:
        form = PaymentForm()
    return render(request, 'restaurant/process_payment.html', {'form': form, 'order': order})

@login_required
def edit_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body)
        payment.payment_method = data.get('payment_method')
        payment.amount = data.get('amount')
        payment.transaction_id = data.get('transaction_id')
        payment.edited_by = request.user
        payment.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from decimal import Decimal
from .models import Order, MenuItem, OrderItem

@login_required
def add_order_item(request, order_id):
    if request.method == 'POST':
        try:
            order = get_object_or_404(Order, order_id=order_id)
            
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity', 1))
            
            if quantity < 1:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Quantity must be positive'
                }, status=400)
            
            menu_item = get_object_or_404(MenuItem, id=item_id, is_available=True)
            
            # Check if item already exists in order
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                item=menu_item,
                defaults={
                    'quantity': quantity,
                    'price': menu_item.price
                }
            )
            
            if not created:
                order_item.quantity = quantity
                order_item.save()
            
            # Recalculate order total
            order_items = order.items.all()
            total_amount = sum(item.price * item.quantity for item in order_items)
            order.total_amount = total_amount
            order.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Item added successfully',
                'new_total': str(total_amount),
                'item_html': {
                    'name': menu_item.name,
                    'quantity': order_item.quantity,
                    'price': str(menu_item.price),
                    'total': str(order_item.price * order_item.quantity),
                    'item_id': order_item.id
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)



@login_required
def remove_order_item(request, order_id, item_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_id=order_id)
        order_item = get_object_or_404(OrderItem, id=item_id, order=order)
        
        try:
            # Calculate the reduction in total amount
            reduction = order_item.price * order_item.quantity
            
            # Delete the order item
            order_item.delete()
            
            # Update the order's total amount
            order.total_amount -= reduction
            order.save()
            
            return JsonResponse({
                'status': 'success',
                'new_total': str(order.total_amount)
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@login_required
def update_order_items(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        try:
            total_amount = 0
            for item in order.items.all():
                quantity = request.POST.get(f'quantity_{item.id}')
                if quantity is not None:
                    item.quantity = int(quantity)
                    item.save()
                    total_amount += item.price * item.quantity
            
            order.total_amount = total_amount
            order.save()
            return JsonResponse({'success': True, 'new_total': str(total_amount)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def transaction_history(request):
    orders = OrderHistory.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
        'payment_method_choices': Payment.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'restaurant/transaction_history.html', context)

from django.http import JsonResponse

def get_order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    response_data = {
        'order_id': order.id,
        'customer_name': order.customer.name,
        'customer_phone': order.customer.phone,
        'order_type': order.order_type,
        'table': {'number': order.table.number} if order.table else None,
        'completed_by': order.completed_by.name if order.completed_by else None,
        'total_amount': order.total_amount,
        'payment_status': order.payment_status,
        'created_at': order.created_at,
        'updated_at': order.updated_at,
        'special_notes': order.special_notes,
    }
    return JsonResponse(response_data)

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    categories = Category.objects.filter(is_active=True)
    menu_items = MenuItem.objects.filter(is_available=True)
    
    context = {
        'order': order,
        'categories': categories,
        'menu_items': menu_items,
        'payment_methods': Payment.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'restaurant/order_detail.html', context)


from .models import Order, OrderHistory, OrderHistoryItem


def move_to_history(self):
    if self.status == 'completed' and self.payment_status == 'paid':
        # First, create the OrderHistory instance
        order_history = OrderHistory.objects.create(
            order_id=self.order_id,
            customer_name=self.customer_name,
            customer_phone=self.customer_phone,
            order_type=self.order_type,
            status=self.status,
            total_amount=self.total_amount,
            payment_status=self.payment_status,
            special_notes=self.special_notes,
            table=self.table,
            completed_by=self.completed_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        
        # Copy order items to OrderHistoryItem
        for order_item in self.items.all():
            try:
                OrderHistoryItem.objects.create(
                    order_history=order_history,
                    item=order_item.item,
                    quantity=order_item.quantity,
                    price=order_item.price
                )
            except Exception as e:
                print(f"Error copying order item: {e}")
        
        # Only delete the original order after successfully copying everything
        try:
            self.delete()
        except Exception as e:
            print(f"Error deleting original order: {e}")
        
        return order_history
    return None


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import OrderHistory, OrderHistoryItem



@login_required
def order_history_details(request, order_id):
    try:
        order = get_object_or_404(OrderHistory, order_id=order_id)
        
        # Get all order items
        order_items = order.items.all().select_related('item')
        items_data = []
        for item in order_items:
            try:
                item_data = {
                    'item_name': item.item.name,
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'total': float(item.price * item.quantity)
                }
                items_data.append(item_data)
            except Exception as e:
                print(f"Error processing item: {e}")
        
        # Get payment details
        payment_data = []
        payment_method_dict = dict(Payment.PAYMENT_METHOD_CHOICES)
        for payment in order.payment_details:
            payment_data.append({
                'method': payment_method_dict.get(payment.payment_method, 'Unknown'),
                'amount': float(payment.amount),
                'transaction_id': payment.transaction_id
            })
        
        # Add table information if it's a table order
        table_data = None
        if order.order_type == 'table' and order.table:
            table_data = {
                'number': order.table.number,
                'capacity': order.table.capacity
            }
        
        data = {
            'order_id': str(order.order_id),
            'customer_name': order.customer_name,
            'customer_phone': order.customer_phone,
            'order_type': order.order_type,
            'table': table_data,
            'total_amount': float(order.total_amount),
            'payments': payment_data,
            'completed_by': str(order.completed_by.get_full_name()) if order.completed_by else None,
            'special_notes': order.special_notes,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat(),
            'items': items_data
        }
        
        return JsonResponse(data)
    except Exception as e:
        print(f"Error in order_history_details: {e}")
        return JsonResponse({
            'error': 'Failed to fetch order details',
            'message': str(e)
        }, status=500)



from .forms import TableForm

class TableListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'restaurant/table_list.html'
    context_object_name = 'tables'

class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'restaurant/table_form.html'
    success_url = reverse_lazy('restaurant:table_list')

class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'restaurant/table_form.html'
    success_url = reverse_lazy('restaurant:table_list')

class TableDeleteView(LoginRequiredMixin, DeleteView):
    model = Table
    template_name = 'restaurant/table_confirm_delete.html'
    success_url = reverse_lazy('restaurant:table_list')

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'restaurant/menuitem_list.html'
    context_object_name = 'menu_items'

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'restaurant/menuitem_form.html'
    success_url = reverse_lazy('restaurant:menuitem_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter out inactive categories
        form.fields['category'].queryset = Category.objects.filter(is_active=True)
        return form

from django.core.paginator import Paginator

def transaction_history(request):
    orders_list = OrderHistory.objects.all().order_by('-created_at')
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page
    
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
        'payment_method_choices': Payment.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'restaurant/transaction_history.html', context)


class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'restaurant/menuitem_form.html'
    success_url = reverse_lazy('restaurant:menuitem_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter out inactive categories but include the current category if inactive
        form.fields['category'].queryset = Category.objects.filter(
            models.Q(is_active=True) | models.Q(pk=self.object.category_id)
        )
        return form

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'restaurant/menuitem_confirm_delete.html'
    success_url = reverse_lazy('restaurant:menuitem_list')

class MenuItemDetailView(LoginRequiredMixin, DetailView):
    model = MenuItem
    template_name = 'restaurant/menuitem_detail.html'
    context_object_name = 'menu_item'

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'restaurant/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'restaurant/category_form.html'
    success_url = reverse_lazy('restaurant:category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'restaurant/category_form.html'
    success_url = reverse_lazy('restaurant:category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'restaurant/category_confirm_delete.html'
    success_url = reverse_lazy('restaurant:category_list')

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'restaurant/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']