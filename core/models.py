from django.db import models

# Create your models here.

class Kit(models.Model):
    identification = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    roof = models.CharField(max_length=255)
    connection = models.CharField(max_length=255)
    maximum_overload = models.PositiveIntegerField()
    kwp = models.DecimalField(decimal_places=3, max_digits=9)
    modules = models.ManyToManyField("Module", through="KitModule", related_name="kits")
    inverters = models.ManyToManyField("Inverter", through="KitInverter", related_name="kits")
    cables = models.ManyToManyField("Cable", through="KitCable", related_name="kits")
    connector_pairs = models.ManyToManyField("ConnectorPair", through="KitConnectorPair", related_name="kits")
    string_boxes = models.ManyToManyField("StringBox", through="KitStringBox", related_name="kits")
    structures = models.ManyToManyField("Structure", through="KitStructure", related_name="kits")

class Module(models.Model):
    model = models.CharField(max_length=255)
    power = models.PositiveIntegerField()
    brand = models.CharField(max_length=255)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["model", "power", "brand"], name="unique_model_power_brand")]

class Inverter(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "brand"], name="unique_name_brand")]

class Cable(models.Model):
    model = models.CharField(max_length=255, unique=True)

class ConnectorPair(models.Model):
    model = models.CharField(max_length=255, unique=True)

class StringBox(models.Model):
    model = models.CharField(max_length=255, unique=True)

class Structure(models.Model):
    model = models.CharField(max_length=255, unique=True)

class KitModule(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="kit_modules")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="kit_modules")
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kit", "module"], name="unique_kit_module")]

class KitInverter(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="kit_inverters")
    inverter = models.ForeignKey(Inverter, on_delete=models.CASCADE, related_name="kit_inverters")
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kit", "inverter"], name="unique_kit_inverter")]

class KitCable(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="kit_cables")
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, related_name="kit_cables")
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kit", "cable"], name="unique_kit_cable")]

class KitConnectorPair(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="kit_connector_pairs")
    connector_pair = models.ForeignKey(ConnectorPair, on_delete=models.CASCADE, related_name="kit_connector_pairs")
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kit", "connector_pair"], name="unique_kit_connectorpair")]

class KitStringBox(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="kit_string_boxes")
    string_box = models.ForeignKey(StringBox, on_delete=models.CASCADE, related_name="kit_string_boxes")
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kit", "string_box"], name="unique_kit_stringbox")]

class KitStructure(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name="kit_structures")
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, related_name="kit_structures")
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kit", "structure"], name="unique_kit_structure")]
