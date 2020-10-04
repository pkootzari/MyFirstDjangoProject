from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.contrib import messages


def createNewUser(username, password, email, phoneNumber):
    user = models.User.objects.create_user(username, password=password)
    profile = models.Profile.objects.create(user=user)
    models.ContactInfo.objects.create(user=profile, email=email, phone=phoneNumber)
    return user


def createNewService(form, request):
    user = request.user.profile
    form = models.Service.objects.create(serviceName=form['name'], fee=form['fee'], user=user)


def createNewOrder(form, user):
    order = models.Order.objects.create(user=user.profile)
    for service in models.Service.objects.all():
        if form.get(service.serviceName) == 'on':
            print("bos")
            order.services.add(service)
    order.calculateCost()
    invoice = models.Invoice.objects.create(paid=0)
    order.factor = invoice
    invoice.calculateTotalCost()
    invoice.calculateDebt()
    invoice.save()
    order.save()


def createNewTicket(form, user):
    ticket = models.Ticket.objects.create(title=form['title'], creator=user, status=1)
    models.Message.objects.create(ticket=ticket, author=user, body=form['body'])


def homePage(request):
    if request.user.is_authenticated:
        return redirect('company:userpage')
    if request.method == 'POST':
        form = request.POST
        user = authenticate(request,  password=form['password'], username=form['username'])
        if user is not None:
            login(request, user)
            messages.success(request, 'You Logged in successfully!')
            return redirect("company:userpage")
        else:
            messages.error(request, 'Wrong Username or Password')
            return redirect('company:login')
    return render(request, 'companymodels/homepage.html')


def newUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Log out first')
        return redirect('company:userpage')
    if request.method == 'POST':
        form = request.POST
        try:
            user = createNewUser(form['username'], form['password'], form['email'], form['phone'])
            user = authenticate(request, username=form['username'], password=form['password'])
            login(request, user)
            messages.success(request, 'Your account created successfully and you\'re logged in!')
            return redirect('company:userpage')
        except Exception:
            messages.error(request, 'Can\'t make your account!')
    return render(request, 'companymodels/newuser.html')


@login_required()
def userPage(request):
    user = request.user.profile
    if request.method == 'POST':
        orderID = request.POST['orderID']
        models.Order.objects.get(id = orderID).delete()
    orders = user.orders.all()
    service = models.Service.objects.all()
    tickets = user.tickets.all()
    allTickets = models.Ticket.objects.all()
    context = {'orders': orders, 'services': service, 'tickets': tickets, 'allTickets': allTickets}
    return render(request, 'companymodels/userpage.html', context)


@login_required()
def logout(request):
    django_logout(request)
    messages.success(request, 'You logged out successfully!')
    return redirect('company:login')


@login_required()
def newOrder(request):
    user = request.user
    if request.method == 'POST':
        form = request.POST
        createNewOrder(form, user)
        messages.success(request, 'You order added successfully!')
        return redirect('company:userpage')
    context = {'services': models.Service.objects.all()}
    return render(request, 'companymodels/neworder.html', context)


@login_required()
def newService(request):
    if not request.user.is_superuser:
        messages.warning(request, 'Access Denied')
        return redirect('company:userpage')
    if request.method == 'POST':
        form = request.POST
        try:
            createNewService(form, request)
            messages.success(request, 'You\'re service added succssfully!')
            return redirect('company:userpage')
        except Exception:
            messages.error(request, 'Could\'nt add the service')
    return render(request, 'companymodels/newservice.html')


@login_required()
def newTicket(request):
    if request.method == 'POST':
        form = request.POST
        user = request.user.profile
        try:
            createNewTicket(form, user)
            messages.success(request, 'Your Ticket successfully sent!')
            return redirect('company:userpage')
        except Exception:
            messages.error(request, 'Can\'t make your ticket!')
    return render(request, 'companymodels/newticket.html')


@login_required()
def ticketReview(request):
    user = request.user
    if user.is_superuser:
        tickets = models.Ticket.objects.all()
    else:
        tickets = user.profile.tickets.all()
    context = {'tickets': tickets}
    return render(request, "companymodels/ticketreview.html", context)
