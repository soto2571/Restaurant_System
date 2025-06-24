from django.shortcuts import render, redirect
from .models import Table, Account, OrderNote
from .forms import OrderNoteForm, AccountForm

"""
Views for the app to handle landing page, waiter dashboard, kitchen dashboard,
"""

def landing_page(request):
    return render(request, 'orders/landing_page.html')

def waiter_dashboard(request):
    tables = Table.objects.all()
    return render(request, 'orders/waiter_dashboard.html', {'tables': tables})

def kitchen_dashboard(request):
    orders = OrderNote.objects.all().order_by('created_at')
    return render(request, 'orders/kitchen_dashboard.html', {'orders': orders})



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