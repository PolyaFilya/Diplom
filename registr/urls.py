from django.urls import path


from . import views

urlpatterns = [
    #ex: /registr/
    path('', views.index, name='index'),
    #ex: /registr/choice
    path('choice/', views.choice, name='choice'),
    #ex: /registr/5/new_user
    path('<int:event_id>/new_user', views.new_user, name='new_user'),
    #ex: /registr/5/done
    path('<int:user_id>/done/', views.reg_done, name='reg_done'),
    #wx: /registr/5/done/qr
    path('<int:user_id>/done/qr/', views.qr, name='qr'),
    #ex: /registr/scan
    path('scan/', views.scan, name='scan'),
    #ex: /registr/100/here
    path('<int:user_id>/here/', views.user_here, name='user_here'),
]
