from django import forms
from teacher.models import Problem

class ModelFormWithFileField(forms.ModelForm):
    class Meta:
        model = Problem
        fields = '__all__'
        exclude = ('teacher',)