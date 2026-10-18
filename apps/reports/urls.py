from django.urls import path

from .views import ReportDetailView

app_name = 'reports'

urlpatterns = [
    path('reportes/<slug:report>/', ReportDetailView.as_view(), name='detail'),
]
