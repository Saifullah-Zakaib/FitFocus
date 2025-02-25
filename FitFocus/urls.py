from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('exlog/', include('Exercise_tracker.urls')),
]
