from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username


class ContactInfo(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='contactinfo')
    email = models.EmailField(max_length=20)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.user.user.username + "::" + self.email + "::" + self.phone


class Service(models.Model):
    serviceName = models.CharField(max_length=30)
    fee = models.PositiveIntegerField()

    def __str__(self):
        return self.serviceName + "::" + str(self.fee)


class Invoice(models.Model):
    totalCost = models.PositiveIntegerField(blank=True, null=True)
    paid = models.PositiveIntegerField(blank=True, null=True)
    debt = models.PositiveIntegerField(blank=True, null=True)

    def calculateTotalCost(self):
        self.totalCost = self.order.cost

    def calculateDebt(self):
        self.debt = int(self.totalCost) - int(self.paid)

    def __str__(self):
        return 'Total Cost : ' + str(self.totalCost) + ' To Pay : ' + str(self.debt)


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    factor = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='order', blank=True, null=True)
    cost = models.PositiveIntegerField(blank=True, null=True)
    services = models.ManyToManyField(Service, related_name='orders', blank=True, null=True)

    def calculateCost(self):
        self.cost = 0
        for s in self.services.all():
            self.cost += s.fee

    def __str__(self):
        string = str(self.user) + '\n'
        for service in self.services.all():
            string += str(service)
            string += '\n'
        return string


class Ticket(models.Model):
    choices = [(1, 'responded'),
               (2, 'notResponded')]
    status = models.CharField(choices=choices, max_length=32)
    title = models.TextField()
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tickets')

    def __str__(self):
        return self.title + " :: Status : " + self.status


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()

    def __str__(self):
        return self.author + "::" + self.body
