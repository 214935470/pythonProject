from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from .forms import AddUserForm, MassageForm,ApartmentForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, logout, authenticate
from .models import Apartment,Image,message
# Create your views here.
def Register(request):
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                login(request, user)
                return redirect('login')
        else:
            form = AddUserForm()

        return render(request, 'Register.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.isBuyer==False:
                    return redirect('/broker')
                else:
                    return redirect('/buyer')
            else:
                return redirect('/')

    else:
        form = AuthenticationForm()
    return render(request, 'Login.html', {'form': form})
@login_required
def Broker(request):
    if request.user.isBuyer:
        return redirect('/')
    if not request.user.is_authenticated:
        return render(request, 'Brokers_apartments.html', {'error': 'עליך להיות מחובר כדי לצפות בדירות שלך.'})
    apartments = Apartment.objects.filter(userId=request.user)
    images = Image.objects.filter(apartmentId__in=apartments)
    if not apartments.exists():
        return render(request, 'Brokers_apartments.html', {'error': 'לא נמצאו דירות למשתמש המחובר.'})
    return render(request,'Brokers_apartments.html',{'apartments':apartments,'images':images})
@login_required
def Buyer(request):
    apartments = Apartment.objects.filter(status=False)
    if request.method == 'POST':
        city = request.POST.get('city')
        floor = request.POST.get('floor')
        price = request.POST.get('price')

        if city:
            apartments = apartments.filter(city=city)
        if floor:
            apartments = apartments.filter(floor__lte=floor)
        if price:
            apartments = apartments.filter(price__lte=price)
    images=Image.objects.all()
    data={
        'apartment': apartments,
        'images': images
    }
    return render(request,'Apartments_for_sale.html',data)
@login_required
def contact_seller(request, apartment_id):
    form = MassageForm()
    # apartment = get_object_or_404(Apartment, userId = apartment_id.userId)  # מציאת הדירה לפי user_id
    apartment = Apartment.objects.get(id = apartment_id)
    if request.method == 'POST':
        form = MassageForm(request.POST)
        if form.is_valid():
            # יצירת הודעה חדשה ושיוכה לדירה
            new_message = form.save(commit=False)
            new_message.apartmentId = apartment
            new_message.save()
            return redirect('/buyer')
    # לוגיקה לטיפול בבקשה לפנייה למוכר
    return render(request, 'Massage.html', {'user_id': apartment_id,'form': form})
@login_required
def New_Apartment(request):
    if request.user.isBuyer:
        return redirect('/')
    form = ApartmentForm()

    if request.method == 'POST':
        form = ApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.userId = request.user  # מקשר את הדירה למשתמש המחובר
            apartment.save()

            # שמור את התמונות
            images = request.FILES.getlist('images')
            for image in images:
                Image.objects.create(apartmentId=apartment, image=image)
            return redirect('/broker')

    # לוגיקה לטיפול בבקשה לפנייה למוכר
    return render(request, 'NewApartment.html', {'form': form})

@login_required
def GetMassages(request, apartment_Id):
    if request.user.isBuyer:
        return redirect('/')
    messages = message.objects.filter(apartmentId_id=apartment_Id)
    return render(request, 'GetMessage.html', {'messages': messages})
@login_required
def mark_sold(request, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    apartment.status = True
    apartment.save()
    if not request.user.is_authenticated:
        return render(request, 'Brokers_apartments.html', {'error': 'עליך להיות מחובר כדי לצפות בדירות שלך.'})
    apartments = Apartment.objects.filter(userId=request.user)
    images = Image.objects.filter(apartmentId__in=apartments)
    if not apartments.exists():
        return render(request, 'Brokers_apartments.html', {'error': 'לא נמצאו דירות למשתמש המחובר.'})
    return render(request, 'Brokers_apartments.html', {'apartments': apartments, 'images': images})
    return render(request,  'Brokers_apartments.html')