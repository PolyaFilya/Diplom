from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from urllib.request import urlopen


import cv2
import qreader
from .qr import make_qr_code

from .models import User, Event, State, QR
from .forms import QRForm

def index(request):
    event_list = Event.objects.all()
    context = { 'event_list': event_list }
    return render(request, 'registr/index.html', context)

def choice(request, event_id):
    event = Event.objects.get(pk=event_id)
    event_name = event.event_name
    new_user_id = User.objects.latest('id').id + 1
    context = { 
        'event_name': event_name,
        'user_id': new_user_id,
        'event_id': event_id,
    }
    return render(request, 'registr/choice.html', context)

def new_user(request, event_id):
    new_user_id = User.objects.latest('id').id + 1
    #тут типа должно быть добавление данных в учетную запись
    try:
        new_user = User.objects.create(first_name=request.POST['name'], gender=request.POST['gender'], email=request.POST['email'], age=request.POST['age'], event_id=request.POST['event_id'])
        reg_state = new_user.state_set.create(name_state="reg", user_id=new_user.id, reg_time=timezone.now())
    except (KeyError, User.DoesNotExist):
        return render(request, 'registr/new_user.html', {
            'user_id': new_user_id,
            'error_message': "Вы не ввели данные",
        })
    else:
        return HttpResponseRedirect(reverse('reg_done', args=(new_user.id,)))

def reg_done(request, user_id):
    try:
        user = User.objects.latest('id')
        first_name = user.first_name
        event = Event.objects.get(id=user.event_id)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'registr/reg_done.html', { 'first_name': first_name, 'event': event, 'user': user,})

def qr(request, user_id):
    qr = make_qr_code(user_id)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response

def scan(request, event_id):
    event = Event.objects.get(pk=event_id)
    # тут еще типа надо вставить сканирование QR, получение id пользователя
    if request.method == 'POST':
        form = QRForm(request.POST, request.FILES)
        if form.is_valid():
            #тут должна быть выгрузка файла из формы 
            qr = QR()
            qr.file = form.cleaned_data["file"]
            qr.file.save('qr.png', content=qr.file, save=True)
            user_id = qreader.read('registr/files/qrs/qr.png')
            user = User.objects.get(pk=user_id)
            user.state_set.create(name_state="here", user_id=user.id, reg_time=timezone.now())
            qr.file.delete()
            return HttpResponseRedirect(reverse('user_here', args=(user_id, )))
    else:
        form = QRForm()

    return render(request, 'registr/scan.html', {'form': form, 'event': event })

def user_here(request, user_id):
    try:
        first_name = User.objects.get(pk=user_id).first_name
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'registr/user_here.html', { 'first_name': first_name })
