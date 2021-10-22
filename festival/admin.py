from django.contrib import admin
from .models import *

admin.site.register(Photo)
admin.site.register(Story)
admin.site.register(StoryComment)
admin.site.register(PhotoComment)
