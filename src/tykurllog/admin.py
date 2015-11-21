from django.contrib import admin
from django.apps import apps

### register all models in this app in the admin
for model in apps.get_app_config('tykurllog').get_models():
    admin.site.register(model)

