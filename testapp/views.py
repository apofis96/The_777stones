from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import Game #пошо надо документацию на 2,0 читать!
#from userStatistics.views import
from .models import Notification
from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    return render(
        request,
        'index.html',
    )

@login_required()
def home(request):
    notify = Notification.objects.filter(playerID=request.user)
    var = notify.count()
    if (request.method == 'POST'):
        kok = request.POST.get('close')
        Notification.objects.filter(pk=kok).delete()
        return HttpResponseRedirect('/home')
    return render(request, 'home.html', {'notify' : notify, 'var':var} )

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "accounts/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/registration.html"


    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
