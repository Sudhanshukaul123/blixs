from django.contrib import admin
from django.apps import apps
# Register your models here.
models = apps.get_app_config("api").get_models()
for modle in models :
    try:
      admin.site.register(modle)
    except admin.site.AlreadyRegistered :
       pass
      