from django.db import models

# Django models
# People database
class People_db(models.Model):
    _id = models.TextField(blank=True, null=True)
    index = models.TextField(blank=True, null=True)
    guid = models.TextField(blank=True, null=True)
    has_died = models.TextField(blank=True, null=True)
    balance = models.TextField(blank=True, null=True)
    picture = models.TextField(blank=True, null=True)
    age = models.TextField(blank=True, null=True)
    eye_color = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    company_id = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    registered = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    friends = models.TextField(blank=True, null=True)
    greeting = models.TextField(blank=True, null=True)
    favourite_food = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'People database'

# Companies database
class Companies_db(models.Model):
    index = models.TextField(blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = 'Companies database'