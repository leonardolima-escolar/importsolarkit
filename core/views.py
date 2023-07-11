from django.views import View
from django.views.generic import ListView

from core.models import Kit

# Create your views here.


class SolarPanelKits(ListView):
    model = Kit

class ImportToTheDatabase(View):
    def post(self, request):
        return

