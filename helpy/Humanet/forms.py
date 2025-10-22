from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from .models import PerfilUsuario, Evento

class RegistroForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario')
    first_name = forms.CharField(label='Nombres', max_length=30)
    last_name = forms.CharField(label='Apellidos', max_length=30)
    email= forms.CharField(label='Correo electronico')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, help_text=_("Debe tener al menos 8 caracteres."))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, help_text=_("Ingrese la misma contraseña para verificación."))

    numero_celular = forms.CharField(label='Número celular', max_length=9)
    biografia = forms.CharField(label='Biografía', widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), required=True)
    foto = forms.ImageField(label='Foto de perfil', required=False) 

    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','username', 'password1', 'password2']
        widgets = {
        'email': forms.EmailInput(attrs={'autocomplete': 'email'})
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if ' ' in username:
            raise forms.ValidationError("El nombre de usuario no puede contener espacios.")
        if len(username) < 5:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 5 caracteres.")
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', first_name):
            raise forms.ValidationError("El nombre solo puede contener letras.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', last_name):
            raise forms.ValidationError("El apellido solo puede contener letras.")
        return last_name
    
class EventoForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Fecha del evento'
    )
    
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        }),
        label='Hora del evento'
    )
    
    class Meta:
        model = Evento
        fields = ['nombre', 'fecha', 'hora', 'ubicacion', 'latitud', 'longitud', 
                  'descripcion', 'detalles']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Jornada de limpieza comunitaria'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Plaza principal, Villa Alemana'}),
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe brevemente el evento...'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Información adicional, materiales necesarios, etc.'}),
            
        }
        labels = {
            'nombre': 'Nombre del evento',
            'ubicacion': 'Ubicación',
            'descripcion': 'Descripción',
            'detalles': 'Detalles adicionales',
            
        }