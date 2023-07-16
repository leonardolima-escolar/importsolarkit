from django.core.exceptions import ValidationError
import pandas as pd
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.db import transaction

from core.models import (Kit, Module, Inverter, Cable, ConnectorPair, StringBox, 
                        Structure, KitModule, KitInverter, KitCable,
                        KitConnectorPair, KitStringBox, KitStructure)

# Create your views here.


class SolarPanelKits(ListView):
    model = Kit
    paginate_by = 20

class ImportToTheDatabase(View):
    success_url = reverse_lazy('solar_panel_kits')

    def get(self, request):
        return render(request, 'core/import_to_the_database.html')

    def post(self, request):
        excel_file = request.FILES['file']
        df = pd.read_excel(excel_file)
        df = df.drop('Coluna1', axis=1)
        if not all(df.columns.isin(['Identificação Kit', 'Código', 'Preço', 'Telhado', 
                              'Conexão', 'Quant. Módulos', 'Modelo Módulo', 
                              'Potência Wp Unitária Módulo', 'Overload Máximo',
                              'kWp', 'Qtde. Inversor 1', 'Inversor 1',
                              'Qtde. Inversor 2', 'Inversor 2', 
                              'Quant. Cabo Vermelho (m)',
                              'Modelo Cabo Vermelho', 'Quant. Cabo Preto (m)', 
                              'Modelo Cabo Preto', 'Quant. Pares Conectores',
                              'Modelo Par Conector', 'Quant. Stringbox', 
                              'Modelo Stringbox', 'Quant. Estrutura 1', 
                              'Modelo Estrutura 1', 'Quant. Estrutura 2', 
                              'Modelo Estrutura 2', 'Quant. Estrutura 3', 
                              'Modelo Estrutura 3', 'Quant. Estrutura 4', 
                              'Modelo Estrutura 4', 'Quant. Estrutura 5', 
                              'Modelo Estrutura 5', 'Marca do Inversor', 
                              'Marca do Módulo'])):
            raise ValidationError('A tabela do Excel não tem as colunas corretas.')
        
        df = validate_and_transform_data(df)

        with transaction.atomic():
            for _, row in df.iterrows():
                kit_data = {
                    'identification': row['Identificação Kit'],
                    'code': row['Código'],
                    'price': row['Preço'],
                    'roof': row['Telhado'],
                    'connection': row['Conexão'],
                    'maximum_overload': row['Overload Máximo'],
                    'kwp': row['kWp'],
                }
                # pylint: disable=E1101
                kit, _ = Kit.objects.get_or_create(code=kit_data['code'], defaults=kit_data)

                module_data = {
                    'model': row['Modelo Módulo'],
                    'power': row['Potência Wp Unitária Módulo'],
                    'brand': row['Marca do Módulo'],
                }
                module, _ = Module.objects.get_or_create(**module_data)
                KitModule.objects.get_or_create(kit=kit, module=module, defaults={'quantity': row['Quant. Módulos']})

                inverter1_data = {
                    'name': row['Inversor 1'],
                    'brand': row['Marca do Inversor'],
                }
                inverter1, _ = Inverter.objects.get_or_create(**inverter1_data)
                KitInverter.objects.get_or_create(kit=kit, inverter=inverter1, defaults={'quantity': row['Qtde. Inversor 1']})

                if row['Qtde. Inversor 2'] > 0 and row['Inversor 2']:
                    inverter2_data = {
                        'name': row['Inversor 2'],
                        'brand': row['Marca do Inversor'],
                    }
                    inverter2, _ = Inverter.objects.get_or_create(**inverter2_data)
                    KitInverter.objects.get_or_create(kit=kit, inverter=inverter2, defaults={'quantity': row['Qtde. Inversor 2']})
                
                cable_data = {
                    'model': row['Modelo Cabo Vermelho'],
                }
                cable, _ = Cable.objects.get_or_create(**cable_data)
                KitCable.objects.get_or_create(kit=kit, cable=cable, defaults={'quantity': row['Quant. Cabo Vermelho (m)']})

                cable_data = {
                    'model': row['Modelo Cabo Preto'],
                }
                cable, _ = Cable.objects.get_or_create(**cable_data)
                KitCable.objects.get_or_create(kit=kit, cable=cable, defaults={'quantity': row['Quant. Cabo Preto (m)']})

                connector_pair_data = {
                    'model': row['Modelo Par Conector'],
                }
                connector_pair, _ = ConnectorPair.objects.get_or_create(**connector_pair_data)
                KitConnectorPair.objects.get_or_create(kit=kit, connector_pair=connector_pair, defaults={'quantity': row['Quant. Pares Conectores']})

                if row['Quant. Stringbox'] > 0:
                    string_box_data = {
                        'model': row['Modelo Stringbox'],
                    }
                    string_box, _ = StringBox.objects.get_or_create(**string_box_data)
                    KitStringBox.objects.get_or_create(kit=kit, string_box=string_box, defaults={'quantity': row['Quant. Stringbox']})

                if row['Quant. Estrutura 1'] > 0:
                    structure_data = {
                        'model': row['Modelo Estrutura 1'],
                    }
                    structure, _ = Structure.objects.get_or_create(**structure_data)
                    KitStructure.objects.get_or_create(kit=kit, structure=structure, defaults={'quantity': row['Quant. Estrutura 1']})

                if row['Quant. Estrutura 2'] > 0:
                    structure_data = {
                        'model': row['Modelo Estrutura 2'],
                    }
                    structure, _ = Structure.objects.get_or_create(**structure_data)
                    KitStructure.objects.get_or_create(kit=kit, structure=structure, defaults={'quantity': row['Quant. Estrutura 2']})
                
                if row['Quant. Estrutura 3'] > 0:
                    structure_data = {
                        'model': row['Modelo Estrutura 3'],
                    }
                    structure, _ = Structure.objects.get_or_create(**structure_data)
                    KitStructure.objects.get_or_create(kit=kit, structure=structure, defaults={'quantity': row['Quant. Estrutura 3']})
                
                if row['Quant. Estrutura 4'] > 0:
                    structure_data = {
                        'model': row['Modelo Estrutura 4'],
                    }
                    structure, _ = Structure.objects.get_or_create(**structure_data)
                    KitStructure.objects.get_or_create(kit=kit, structure=structure, defaults={'quantity': row['Quant. Estrutura 4']})

                if row['Quant. Estrutura 5'] > 0:
                    structure_data = {
                        'model': row['Modelo Estrutura 5'],
                    }
                    structure, _ = Structure.objects.get_or_create(**structure_data)
                    KitStructure.objects.get_or_create(kit=kit, structure=structure, defaults={'quantity': row['Quant. Estrutura 5']})

        return redirect(self.success_url)
    
def validate_and_transform_data(df):
    df.drop_duplicates(subset=['Código'], keep='first', inplace=True)

    for column in ['Identificação Kit', 'Código', 'Telhado', 'Conexão',
                   'Modelo Módulo', 'Inversor 1', 'Inversor 2',
                   'Modelo Cabo Vermelho', 'Modelo Cabo Preto',
                   'Modelo Par Conector', 'Modelo Stringbox',
                   'Modelo Estrutura 1', 'Modelo Estrutura 2',
                   'Modelo Estrutura 3', 'Modelo Estrutura 4',
                   'Modelo Estrutura 5', 'Marca do Inversor',
                   'Marca do Módulo']:
        df[column] = df[column].fillna('').astype(str)
        if len(df[column]) > 255:
            df[column] = df[column].str[:255]

    for column in ['Preço', 'kWp']:
        df[column] = df[column].fillna(0).astype(float)

    for column in ['Quant. Módulos', 'Potência Wp Unitária Módulo',
                   'Overload Máximo', 'Qtde. Inversor 1', 'Qtde. Inversor 2',
                   'Quant. Cabo Vermelho (m)', 'Quant. Cabo Preto (m)',
                   'Quant. Pares Conectores', 'Quant. Stringbox',
                   'Quant. Estrutura 1', 'Quant. Estrutura 2',
                   'Quant. Estrutura 3', 'Quant. Estrutura 4',
                   'Quant. Estrutura 5']:
        df[column] = df[column].fillna(0)
        df[column] = df[column].astype(int)
        df = df[df[column] >= 0]
        
    return df

