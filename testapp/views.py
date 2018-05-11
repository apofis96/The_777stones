from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import Game #пошо надо документацию на 2,0 читать!

# Create your views here.
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = 1
    num_instances = 1
    # Доступные книги (статус = 'a')
    num_instances_available = 1
    num_authors = 1  # Метод 'all()' применен по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors},
    )
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

def allGames(request):

    games = Game.objects.filter(isPublic=True)

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'allgames.html',
        context={'games':games},
    )