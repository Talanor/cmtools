from django.db import models
from django import forms
import django.contrib.auth.models


class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=240)
    consumer_key = models.CharField(max_length=240)
    consumer_secret = models.CharField(max_length=240)

    access_token = models.CharField(max_length=240)
    access_token_secret = models.CharField(max_length=240)

    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)

    def __str__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit is True:
            instance.save()
        return instance

    class Meta:
        model = Client
        fields = [
            'name',
            'consumer_key',
            'consumer_secret',
            'access_token',
            'access_token_secret'
        ]


class Mention(models.Model):
    text = models.CharField(max_length=240)
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    username = models.CharField(max_length=240)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return "<%s: %d>" % (self.__class__.__name__, int(self.id))

    class Meta:
        ordering = ("id",)


class MentionsQueryForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    client_id = forms.IntegerField()

    class Meta:
        fields = ['start_date', 'end_date', 'client_id']
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'id': 'start_date', 'required': True}
            ),
            'end_date': forms.DateTimeInput(
                attrs={'id': 'end_date', 'required': True}
            )
        }
