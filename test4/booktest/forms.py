from django import forms
from captcha.fields import CaptchaField


class CaptchaTestForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    captcha = CaptchaField()
