from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from .models import PerfilUsuario, Evento, Categoria

class RegistroForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario')
    first_name = forms.CharField(label='Nombres', max_length=30)
    last_name = forms.CharField(label='Apellidos', max_length=30)
    email= forms.CharField(label='Correo electronico')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, help_text=_("Debe tener al menos 8 caracteres."))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, help_text=_("Ingrese la misma contraseña para verificación."))

    numero_celular = forms.CharField(label='Número celular', max_length=12, required=False)
    biografia = forms.CharField(label='Biografía', widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Cuéntanos un poco sobre ti o tu organización...'}), required=True)
    foto = forms.ImageField(label='Foto de perfil', required=False) 
    tipo_cuenta = forms.ChoiceField(choices=[('individuo', 'Soy un individuo'), ('organizacion', 'Represento una organización')],
        widget=forms.RadioSelect,
        label='Tipo de cuenta',
        initial='individuo'    )








    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','username', 'password1', 'password2', 'tipo_cuenta']
        widgets = {'email': forms.EmailInput(attrs={'autocomplete': 'email'}) }

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
    
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Categorías del evento',
        help_text='Selecciona al menos una categoría',
        required=True
    )
    
    imagen = forms.ImageField(
        required=False,
        label='Imagen del evento',
        help_text='Formato: JPG, PNG. Tamaño máximo: 5MB',
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    
    class Meta:
        model = Evento
        fields = ['nombre', 'imagen', 'fecha', 'hora', 'region', 'ciudad', 'ubicacion', 
                  'latitud', 'longitud', 'descripcion', 'detalles', 'categorias']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Jornada de limpieza comunitaria'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Villa Alemana'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Plaza principal'}),
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe brevemente el evento...'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Información adicional, materiales necesarios, etc.'}),
        }
        labels = {
            'nombre': 'Nombre del evento',
            'region': 'Región',
            'ciudad': 'Ciudad',
            'ubicacion': 'Ubicación específica',
            'descripcion': 'Descripción',
            'detalles': 'Detalles adicionales',
        }