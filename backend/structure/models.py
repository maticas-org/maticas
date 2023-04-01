from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import PasswordInput


import hashlib


class Org(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    password = models.CharField(max_length=64)  # , widget=PasswordInput())

    def save(self, *arg, **kwargs):
        hash_str = f"{self.password}.{self.name}"
        hash_value = hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

        self.password = hash_value

        super().save(*arg, **kwargs)

    def __str__(self):
        return f"{self.name}.{self.password}"


class Crop(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    coordinate_latitude = models.FloatField()
    coordinate_longitude = models.FloatField()

    def __str__(self):
        return f"{self.name}"


class Variable(models.Model):
    name = models.CharField(max_length=50)
    units = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}.{self.units}"


class Condition(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)

    min_value = models.FloatField()
    max_value = models.FloatField()

    def __str__(self):
        return f"{self.variable}.{self.min_value}.{self.max_value}"


class Actuator_type(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Actuator(models.Model):
    name = models.CharField(max_length=50)
    mqtt_topic = models.CharField(max_length=64)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    actuator_type = models.ForeignKey(Actuator_type, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}.{self.mqtt_topic}"

    def get_state(self):
        """
        Returns the current state of the actuator by querying its MQTT topic.
        """
        # Code to query MQTT topic and return current state of the actuator
        pass

    def set_state(self, state):
        """
        Sets the state of the actuator by publishing a message to its MQTT topic.

        Args:
            - state: The new state to set for the actuator.
        """
        # Code to publish message to MQTT topic to set new state of the actuator
        pass


class Measurement(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    value = models.FloatField()
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.value}.{self.variable}.{self.crop}"


class Permission(models.Model):
    PERMISSION_CHOICES = (
        ('view', 'View'),
        ('edit', 'Edit'),
        ('control', 'Control'),
        ('add', 'Add'),
        ('delete', 'Delete'),
        ('assign', 'Assign Permissions'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    crop = models.ForeignKey(
        Crop, null=True, blank=True, on_delete=models.CASCADE)
    permission_type = models.CharField(
        max_length=10, choices=PERMISSION_CHOICES)
    granted = models.BooleanField(default=False)
    _id = models.CharField(max_length=255, editable=False, unique=True)

    class Meta:
        unique_together = ('user', 'org', 'crop', 'permission_type',)

    def __str__(self):
        return f"{self.user.username} has {self.permission_type} permission for {self.org.name}"

    def save(self, *args, **kwargs):
        conditions = {
            'granted': int(self.granted),
            'user_id': self.user_id,
            'organization_id': self.org_id,
            'permission_type': self.permission_type,
        }
        if self.crop_id is not None:
            conditions['crop_id'] = self.crop_id
        self._id = '_'.join(str(v) for v in conditions.values())
        super().save(*args, **kwargs)
