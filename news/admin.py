from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import News,Category
# Register your models here.

# импортируем для создания редактора в админке
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# класс для создания редактора в админке
class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    # добавляем класс NewsAdminForm
    form=NewsAdminForm
    list_display = ('id','title','category',
                    'created_at','update_at','is_published',
                    'views','get_photo')
    list_display_links = ('id','title')
    search_fields = ('id','title','content')
    list_editable = ('is_published',)
    list_filter = ('is_published','category')
   # Так же можем ее выводит в непосредственно в форме создания новости
   #  то есть когда мы кликаем на новость, чтоб там была не ссылка,
    # а сама фотка
    fields = ('title','category','content','photo', 'get_photo' ,'is_published',
                    'views','created_at','update_at')
    # мы должны сейчас указать поля которые нельзя редактировать,
    # а можно лишь прочесть
    readonly_fields = ('get_photo','views','created_at','update_at')


    def get_photo(self,obj):
        if obj.photo:
            # выведем изображение на админке в списке нвостей
            # в виде html кода. то есть не ссылку, а само изображение
            # чтобы обрабатывал html мы используем функцию mark_safe()
            # внутри фкнции пропишем ссылку img
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return 'Фото не установленно'

    get_photo.short_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')
    search_fields = ('title',)

admin.site.register(News, NewsAdmin)
admin.site.register(Category,CategoryAdmin)


admin.site.site_title='Управления новостями'
#проводим кастомизация админки heaeder
admin.site.site_header='Управления новостями'
# выведем изображение на админке