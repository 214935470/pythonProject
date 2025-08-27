from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("Register", views.Register, name ='Register'),
    path("",views.Login,name ='login'),
path("broker",views.Broker,name ='broker'),
path("buyer",views.Buyer,name ='buyer'),
path("Massage/<int:apartment_id>/",views.contact_seller,name='Massage'),
path("newApartment", views.New_Apartment, name = 'NewApartment'),
path("GetMassages/<int:apartment_Id>", views.GetMassages, name = 'GetMassages'),
path('apartments/<int:apartment_id>', views.mark_sold, name='mark_sold')
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#     path("register", views.Register, name='register'),
#     path("buyer", views.Buyer, name='buyer'),
#     path("saller", views.Saller, name='saller'),
#     path("apply/<int:department_id>", views.Apply, name='apply'),
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)