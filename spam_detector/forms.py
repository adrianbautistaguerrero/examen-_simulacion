from django import forms


class EmailAnalysisForm(forms.Form):
    """
    Formulario para validar el input del usuario.
    """
    email_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Pega aquí el contenido del email que deseas analizar...',
            'required': True
        }),
        label='Contenido del Email',
        help_text='Ingresa el texto completo del email incluyendo headers si los tiene.',
        min_length=10,
        max_length=50000,
        error_messages={
            'required': 'El campo de texto no puede estar vacío.',
            'min_length': 'El email debe tener al menos 10 caracteres.',
            'max_length': 'El email es demasiado largo (máximo 50,000 caracteres).'
        }
    )
