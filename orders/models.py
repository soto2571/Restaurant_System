from django.db import models

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)

class Account(models.Model):
    table = models.ForeignKey(Table, related_name='accounts', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, blank=True)

class OrderNote(models.Model):
    account = models.ForeignKey(Account, related_name='orders', on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)