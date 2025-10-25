from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home
from foodplan_site import views as fp_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('', home, name='home'),
    path('recipes/', fp_views.recipe_list, name='recipes_list'),
    path('recipes/<int:pk>/', fp_views.recipe_detail, name='recipe_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
