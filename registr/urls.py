from django.urls import path


from . import views

urlpatterns = [
    #ex: /registr/
    path('', views.index, name='index'),
    #ex: /registr/1/choice
    path('<int:event_id>/choice/', views.choice, name='choice'),
    #ex: /registr/5
    path('<int:event_id>/new_user', views.new_user, name='new_user'),
    #ex: /registr/5/done
    path('<int:user_id>/done/', views.reg_done, name='reg_done'),
    #wx: /registr/5/done/qr
    path('<int:user_id>/done/qr/', views.qr, name='qr'),
    #ex: /registr/1/scan
    path('<int:event_id>/scan/', views.scan, name='scan'),
    #ex: /registr/1/scan
    #path('<int:user_id>/scan_qr/', views.scan_qr, name='scan_qr'),
    #ex: /registr/100/here
    path('<int:user_id>/here/', views.user_here, name='user_here'),
]
