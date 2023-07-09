from django.contrib import admin
from .models import User, Initiative, Epic, Project, Sprint, Task, UserStory
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

# Register your models here.
admin.site.register(User, UserAdmin)
#admin.site.register(User)
admin.site.register(Initiative)
admin.site.register(Epic)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Task)
admin.site.register(UserStory)

