import pandas as pd
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from core.models import Kit

# Create your views here.


class SolarPanelKits(ListView):
    model = Kit

class ImportToTheDatabase(View):
    def get(self, request):
        return render(request, 'core/import_to_the_database.html')

    def post(self, request):
        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file)
        print(df['Código'])
        return render(request, 'core/kit_list.html')

