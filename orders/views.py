from django.shortcuts import render, redirect
from .models import Table, Account, OrderNote
from .forms import OrderNoteForm, AccountForm
from django.contrib.auth.decorators import login_required

"""
Views for the app to handle landing page, waiter dashboard, kitchen dashboard,
"""
@login_required
def landing_page(request):
    return render(request, 'orders/landing_page.html')

@login_required
def waiter_dashboard(request):
    tables = Table.objects.all()
    return render(request, 'orders/waiter_dashboard.html', {'tables': tables})

@login_required
def kitchen_dashboard(request):
    tables = Table.objects.prefetch_related('accounts__orders').all()
    return render(request, 'orders/kitchen_dashboard.html', {'tables': tables})


"""
Forms views for adding accounts and orders.
"""

def table_detail(request, table_id):
    table = Table.objects.get(id=table_id)
    return render(request, 'orders/table_detail.html', {'table': table})

def add_account(request, table_id):
    table = Table.objects.get(id=table_id)
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.table = table
            account.save()
            return redirect('table_detail', table_id=table_id)
        
    else:
        form = AccountForm()
    return render(request, 'orders/add_account.html', {'form': form, 'table': table})

def add_order(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        form = OrderNoteForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.account = account
            order.save()
            return redirect('table_detail', table_id=account.table.id)
    else:
        form = OrderNoteForm()
    return render(request, 'orders/add_order.html', {'form': form, 'account': account})


"""
Views for editing and deleting accounts.
"""
def edit_account(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('table_detail', table_id=account.table.id)
    else:
        form = AccountForm(instance=account)
    return render(request, 'orders/edit_account.html', {'form': form, 'account': account})


def delete_account(request, account_id):
    account = Account.objects.get(id=account_id)
    table_id = account.table.id
    if request.method == 'POST':
        account.delete()
        return redirect('table_detail', table_id=table_id)
    return render(request, 'orders/delete_account.html', {'account': account})


def clear_table(request, table_id):
    table = Table.objects.get(id=table_id)
    if request.method == 'POST':
        # Clear all accounts and orders for the table
        table.accounts.all().delete()
        return redirect('table_detail', table_id=table_id)
    return render(request, 'orders/clear_table.html', {'table': table})

def edit_order(request, order_id):
    order = OrderNote.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderNoteForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('table_detail', table_id=order.account.table.id)
    else:
        form = OrderNoteForm(instance=order)
    return render(request, 'orders/edit_order.html', {'form': form, 'order': order})

def update_order_status(request, order_id, status):
    order = OrderNote.objects.get(id=order_id)
    if status in ['in_progress', 'completed']:
        order.status = status
        order.save()
    return redirect('kitchen_dashboard')