from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView
from .models import News,Category
from django.urls import reverse_lazy
from .forms import NewsForm
from rest_framework import generics
from.serializers import NewsSerializers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import UserRegisterForm,UserLoginForm,ContactForm
from django.contrib.auth import login,logout
# импортируем send_mail для работы и отправки почты
from django.core.mail import send_mail


# функция для регистрации пользователя

def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            # если мы зарегистрировали пользователя сообщим ему сообшением
            messages.success(request,'Вы успешно зарегистрировались')
            return  redirect('login')
        else:
            # если форма не прошла валидации перейдаем сообщение о ошибке
            messages.error(request,'Ошибка валидации')
    else:
        form=UserRegisterForm()
    return render(request,'news/register.html',{'form':form})

# функция для логина
def user_login(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            # получаем пользователя для авторизации
            user=form.get_user()
            # первый объект запрос, второй аутентифицированный пользователь
            login(request,user)
            # после успешной авторизации делаем redirect()
            return redirect('home')
    else:
        form=UserLoginForm()
    return render(request,'news/login.html',{'form':form})


def user_logout(request):
    logout(request)
    return redirect('login')


# аналог функции def index(request)
# def index(request):
#     news=News.objects.all()
#
#     context={
#         'news':news,
#         'title':'список новостей',
#
#     }
#     return render(request,'news/index.html',context)

# Миксины нам нужны для того чтобы выносить на них
# каккую-то общую логику, которую затем можем использовать
# в различных классов
# Миксины создаются в файле utils.py
# LoginRequiredMixin-используется для ограничения
# доступа не зарегистрированным пользователям

# функция для отправки письма
def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            # форма отправки сообщения:
            # 1)тема, 2)тело, 3)с какой почты , 4)и кому. Для отладки
            # добавляем fail_silently=False. ОН сообщит нам о ошибках
            # Данная функция после отправки письма, выдает 1 в случае успешной отправки письма
            mail=send_mail(form.cleaned_data['subject'],form.cleaned_data['body'],
                      'kamral010101@mail.ru',['kamilmagaramov1991@gmail.com'],
                           fail_silently=False)
            # если мы зарегистрировали пользователя сообщим ему сообшением
            # в случае успешной отправки выдает :Письмо отправлено
            # иначе Ошибка отправки
            if mail:
                messages.success(request,'Письмо отправлено')
                return  redirect('contact')
            else:
                messages.error(request,'Ошибка отправки')
        else:
            # если форма не прошла валидации перейдаем сообщение о ошибке
            messages.error(request,'Ошибка валидации')
    else:
        form=ContactForm()
    return render(request,'news/send_email.html',{'form':form})

#Пагинация проверочная пример функции
def test_pagination(request):
    # берем список для примера
    objects=['kamral1','kamral2','kamral3','kamral4',
            'kamral5','kamral6','kamral7','kamral8','kamral9']
    # создаем объект для пагинации. Сперва нам нужно его импортировать
    # Paginator(objects)-это экземпляр класса Пагинации,а внутри него
    # передаем первым агументов список , а вторым аргументом
    # количество объектов которые должны быть на одной странице
    paginator=Paginator(objects,3)
    # получим номер текущей страницы из объекта request,
    # массива GET, и метод get вернет нам 'page'
    # Параметра page может не быть . И вэтом случае мы можем
    # использовать 1
    page_num=request.GET.get('page',1)
    # чтобы получить нужные объекты для данной страницы.
    # Здесь мы пишем код, чтоб вытаскивать по запросу
    # запрошенную страницу
    page_objects=paginator.get_page(page_num)
    # обрабатываем шаблон
    return render(request,'news/test.html',{'page_obj':page_objects})


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    # мы меняем имя object_list-которая в шаблоне стоит по умолчанию на news
    context_object_name = 'news'
    # пагинация-по 3 записи на 1 страницу
    paginate_by = 3
    # Для того чтобы фильтровать данные , мы воспользуемся
    # функцией get_queryset. Сейчас мы выводим только те посты
    # которые были опубликованны
    # в select_related('')- указываем наше поле для связи

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# def get_category(request, category_id):
#     news=News.objects.filter(category_id=category_id)
#
#     category=Category.objects.get(pk=category_id)
#     return render(request,'news/category.html',
#                   {'news':news, 'category':category})


# Аналог функции get_category()
class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'



#
# def view_news(request,news_id):
#     # news_item=News.objects.get(pk=news_id)
#     news_item=get_object_or_404(News,pk=news_id)
#     return render(request,'news/view_news.html', {'news_item':news_item})

# Аналог функции view_news()
# Универсальное подробное представление NewsDeatail должно вызываться
# либо с объектом pk, либо со слагом в URLconf.
class NewsDeatail(DetailView):
    model = News
    # Универсальное подробное представление NewsDeatail должно вызываться
    # либо с объектом pk, либо со слагом в URLconf.
    # Такая ошибка вышла так ка мы передаем в urls -<int:news_id>,
    # а django требует <int:pk>-мы можем изменить ошибку в ulrs,
    # или переопределить с помощью pk_url_kwarg = 'news_id
    # pk_url_kwarg = 'news_id'
    template_name ='news/news_detail.html'
    context_object_name = 'news_item'

# def add_news(request):
#     # мы проверяем пришли ли   данные с методом формы - POST
#     if request.method == 'POST':
#         # мы создаем обект формы и заполняем его данными из post
#         form=NewsForm(request.POST)
#         # после того как мы полуичили форму , она уже связанна.
#         # мы можем проверять прошла ли она валидацию. Для этого используется
#         # такой метод как is_valid
#         if form.is_valid():
#             # Если форма прошла валидацию,
#             # можем сохранить ее сохранить
#             # news-будет возвращать объект созданной записи
#             news=form.save()
#             # после отправки формы , с помощью redirect
#             # мы  переходим на созданную нами новость
#             return  redirect(news)
#     # если данным пришли нам методом get,тогда мы создаем пустую форму
#     # то есть не связанную с данными форму-
#     # просто зарашиваю страницу
#     else:
#         form=NewsForm()
#     return render(request,'news/add_news.html',{'form':form})



class NewsCreate(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # reverse_lazy- данная функция перенаправялет нас страницу home
    success_url = reverse_lazy('home')
    login_url = '/admin/'

class NewsApiView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializers

class NewsApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializers
