from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Tripsnew, Alltrips
import bcrypt

# Create your views here.

def LoginReg(request):
    return render(request, 'loginreg.html')

def registration(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')

    hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hash1,
    )
    request.session['user_id'] = new_user.id
    return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors.values():
            messages.error(request, msg)
        return redirect('/')
    users = User.objects.filter(email=request.POST['login_email'])
    if users:
        user=users[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/dashboard')
        messages.error(request, "passwords don't match up!")
    return redirect('/')

def dashboard(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'trips': Tripsnew.objects.all()
    }
    return render(request, 'dashboard.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def tripsnew(request):
    return render(request, 'newtrip.html')

def createtrip(request):
    validations = Tripsnew.objects.trips_validator(request.POST)
    user_from_form = User.objects.get(id=request.session['user_id'])
    if len(validations) > 0:
        for msg in validations.values():
            messages.error(request, msg)
        return redirect('/trips/new')

    Tripsnew.objects.create(
        destination = request.POST['destination'],
        start_date = request.POST['start_date'],
        end_date = request.POST['start_date'],
        plan = request.POST['plan'],
        user = user_from_form
    )
    print(request.POST)
    return redirect('/dashboard')

def delete(request, trip_id):
    deletetrip = Tripsnew.objects.get(id=trip_id)
    deletetrip.delete()
    return redirect('/dashboard')

def cancel(request):
    request.session.clear()
    return redirect('/dashboard')

def edittrip(request, trip_id):
    this_trip = Tripsnew.objects.get(id=trip_id)
    context = {
        'trip': this_trip
    }
    return render(request, 'edittrip.html', context)

def update(request, trip_id):
    validations = Tripsnew.objects.trips_validator(request.POST)
    if len(validations) > 0:
        for msg in validations.values():
            messages.error(request, msg)
        return redirect(f'/trips/edit/{trip_id}')
    updatetrip = Tripsnew.objects.get(id=trip_id)
    updatetrip.destination = request.POST['destination']
    updatetrip.start_date = request.POST['start_date']
    updatetrip.end_date = request.POST['end_date']
    updatetrip.plan = request.POST['plan']
    updatetrip.save()

    return redirect('/dashboard')

def tripdetails(request, trip_id):
    this_trip = Tripsnew.objects.get(id=trip_id)
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'trip': this_trip
    }
    return render(request, 'tripdetails.html', context)