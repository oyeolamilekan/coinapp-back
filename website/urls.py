from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("core.urls"))
]

handler500 = 'core.views.server_error'
handler504 = 'core.views.timeout_error'
handler404 = 'core.views.not_found'
handler400 = 'rest_framework.exceptions.bad_request'