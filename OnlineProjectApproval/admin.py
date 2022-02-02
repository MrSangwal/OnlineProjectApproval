from django.contrib import admin

# Register your models here.

from .models import BRANCH
from .models import STUDENT
from .models import TEACHER
from .models import TITLE
from .models import PROJECT
from .models import PREVPROJECTS

admin.site.register(BRANCH)
admin.site.register(STUDENT)
admin.site.register(TEACHER)
admin.site.register(TITLE)
admin.site.register(PROJECT)
admin.site.register(PREVPROJECTS)