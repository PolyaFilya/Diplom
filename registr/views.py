from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import date
from datetime import time
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from .qr import make_qr_code
from .scanner import scanner

from .models import User, Event, State, QR
from .forms import QRForm

def index(request):
    return render(request, 'registr/index.html')

def choice(request):
    event_list = Event.objects.all()
    context = { 'event_list': event_list }
    return render(request, 'registr/choice.html', context)

def new_user(request, event_id):
    new_user_id = User.objects.latest('id').id + 1
    event = Event.objects.get(pk=event_id)
    #тут типа должно быть добавление данных в учетную запись
    try:
        new_user = User.objects.create(first_name=request.POST['name'], gender=request.POST['gender'], email=request.POST['email'], age=request.POST['age'], event_id=event.id)
        reg_state = new_user.state_set.create(name_state="reg", user_id=new_user.id, reg_time=timezone.now())
    except (KeyError, User.DoesNotExist):
        return render(request, 'registr/new_user.html', {
            'event': event,
            'error_message': "Вы не ввели данные",
        })
    else:
        return HttpResponseRedirect(reverse('reg_done', args=(new_user.id,)))

def reg_done(request, user_id):
    try:
        user = User.objects.latest('id')
        first_name = user.first_name
        event = Event.objects.get(id=user.event_id)
        event_date = event.event_date
        date = event_date.date()
        time = event_date.time()
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'registr/reg_done.html', { 'first_name': first_name, 'event': event, 'user': user, 'date': date, 'time': time, })

def qr(request, user_id):
    qr = make_qr_code(user_id)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response

def scan(request):
    # тут сканирование QR, получение id пользователя
    if request.method == 'POST':
        try:
            form = QRForm(request.POST, request.FILES)
            if form.is_valid():
                #тут должна быть выгрузка файла из формы 
                qr = QR()
                qr.file = form.cleaned_data["file"]
                qr.file.save('qr.png', content=qr.file, save=True)
                try:
                    user_id = scanner('registr/files/qrs/qr.png')
                    if type(user_id) == int:
                        if (user_id <= User.objects.latest('id').id):
                            who = User.objects.get(pk=user_id)
                        else:
                            form = QRForm()
                            error = 'Неправильный QR-код'
                            qr.file.delete()
                            qr.delete()
                            return render(request, 'registr/scan.html', {'form': form, 'error': error})
                    else:
                        form = QRForm()
                        error = 'Неправильный QR-код'
                        qr.file.delete()
                        qr.delete()
                        return render(request, 'registr/scan.html', {'form': form, 'error': error})
                except ValueError:
                    form = QRForm()
                    error = 'Неправильный QR-код'
                    qr.file.delete()
                    qr.delete()
                    return render(request, 'registr/scan.html', {'form': form, 'error': error})
                
                s = who.state_set.count()
                if s == 1:
                    user = User.objects.get(pk=user_id)
                    user.state_set.create(name_state="here", user_id=user.id, reg_time=timezone.now())
                    qr.file.delete()
                    qr.delete()
                    return HttpResponseRedirect(reverse('user_here', args=(user_id, )))      
                else:
                    form = QRForm()
                    error = 'Этот человек уже прошел'
                    qr.file.delete()
                    qr.delete()
                    return render(request, 'registr/scan.html', {'form': form, 'error': error})
        except IndexError:   
            error = 'Это не QR-код'
            qr.file.delete()
            qr.delete()
            return render(request, 'registr/scan.html', {'form': form, 'error': error})
    else:
            form = QRForm()
    


    return render(request, 'registr/scan.html', {'form': form, })

def user_here(request, user_id):
    try:
        first_name = User.objects.get(pk=user_id).first_name   
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return render(request, 'registr/user_here.html', { 'first_name': first_name })
