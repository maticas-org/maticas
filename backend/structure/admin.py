from django.contrib import admin
from .models import *

# Register your models here.
class OrgAdmin(admin.ModelAdmin):
    list_display = (
            "name",
            "description",
            "password",
            )

class CropAdmin(admin.ModelAdmin):
    list_display = (
            "name",
            "org",
            "coordinate_latitude",
            "coordinate_longitude",
            )

class VariableAdmin(admin.ModelAdmin):
    list_display = (
            "name",
            "units",
            "description",
            )

class ConditionAdmin(admin.ModelAdmin):
    list_display = (
            "crop",
            "variable",
            "min_value",
            "max_value",
            )

class Actuator_typeAdmin(admin.ModelAdmin):
    list_display = (
            "name",
            "description",
            )

class ActuatorAdmin(admin.ModelAdmin):
    list_display = (
            "name",
            "mqtt_topic",
            "crop",
            "actuator_type",
            )

class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
            "crop",
            "value",
            "variable",
            )

class PermissionAdmin(admin.ModelAdmin):
    list_display = (
            "_id",
            "user",
            "org",
            "crop",
            "permission_type",
            "granted",
            )


# Register Admin Models
admin.site.register(Org, OrgAdmin)
admin.site.register(Crop, CropAdmin)
admin.site.register(Variable, VariableAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Actuator_type, Actuator_typeAdmin)
admin.site.register(Actuator, ActuatorAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Permission, PermissionAdmin)

