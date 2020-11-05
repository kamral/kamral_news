# Файл для создания миксинов
# Данный класс может принимать и не принимать аргументы
class MyMixin(object):
    mixin_group=''

    def get_prop(self):
        return self.mixin_group.upper()
