from django.urls import path
from . import views

urlpatterns = [
    path('', views.SolarPanelKits.as_view(), name='solar_panel_kits'),
    path('import_to_the_database/', views.ImportToTheDatabase.as_view(), name='import_to_the_database'),
]
