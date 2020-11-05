from django import forms
from .models import Category,News
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# 1-ый способ мы будем использовать модели
# мы наследуемся от ModelForm

class NewsForm(forms.ModelForm):
    # запишем подкласс Meta,в которой мы запишем как должен выглядеть класс
    class Meta:
        # в model-мы указываем какую модель мы будем использовать
        model=News
        # в fields-мы указываем какие поля мы хотим использовать
        fields=['title','content','is_published','category']
        # чтобы поправить форму можно использовать widget-которая позволит
        # нам использовать form-control и другие конфигурации
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'rows':5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

# для регистрации
class UserRegisterForm(UserCreationForm):
    # переопределяем поля
    username=forms.CharField(label='Имя пользователя',
                             widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Подтверждения пароля',
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    # добавляем дополн.поля.
    email=forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class':'form-control'}))
    # настройка формы
    class Meta:
        # модель с которым будет связанна форма
        model=User
        # какие поля и в каком порядке должны быть представлены
        fields=('username','password1','password2')


# создания класса для авторизации

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))


#  # 2-способ когда создаем форму не привязанную с моделями
# class NewsForm(forms.Form):
#
#     # создаем widget-для передачи атрибутов в нужное нам поле в TextInput,
#     # в виде словаря через attrs. ОН нужен чтобы дополнительно добавлять  настройки.
#     title = forms.CharField(max_length=150,label='Название',
#                             widget=forms.TextInput(attrs={'class':'form-control'}))
#     # required=False-чтобы сделать поле необязательным
#     content = forms.CharField(label='Текст',required=False,
#                               widget=forms.Textarea(attrs={
#                                   'class':'form-control',
#                               'rows':5}))
#     # initial-по умолчанию делает отмечанный
#     is_published = forms.BooleanField(label='Опубликованно?', initial=True)
#     # empty lable-нужно чтоб в выпадающем списке был текст 'выберите категорию'
#     category = forms.ModelChoiceField(label='Категория',
#                                       empty_label='Выберите категорию',
#                                       queryset=Category.objects.all(),
#     # для того чтобы это был выпадающий список мы используем Select
#                                       widget=forms.Select(attrs={'class':'form-control'}))
#
#
#

# создаем класс для отправки почты

class ContactForm(forms.Form):
    # тема письма
    subject = forms.CharField(label='Тема письма',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    # тело письма
    body = forms.CharField(label='Тело письма',
                              widget=forms.Textarea(
                                  attrs={'class': 'form-control','rows':5}))






