from django.contrib import admin
from django.urls import path
from django.urls import include

from django.conf import settings
from django.conf.urls.static import static

app_name = 'financial_log'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wallet_app/', include('wallet_app.urls')),
    path('diary_app/', include('diary_app.urls')),
    path('calendar_app/', include('calendar_app.urls')),
    path('statistics_app/', include('statistics_app.urls')),
    path('wordcloud_app/', include('wordcloud_app.urls'))
] 
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)