from django.shortcuts import render, redirect
from .models import GeneratedPassword
import string
import secrets


def generate_password(length=12, use_letters=True, use_digits=True, use_special_chars=True):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        return "Please select at least one character type."

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def index(request):
    generated_password = None
    if request.method == 'POST':
        password_length = int(request.POST.get('password_length', 12))
        use_letters = 'use_letters' in request.POST.getlist('features')
        use_digits = 'use_digits' in request.POST.getlist('features')
        use_special_chars = 'use_special_chars' in request.POST.getlist('features')

        generated_password = generate_password(
            length=password_length,
            use_letters=use_letters,
            use_digits=use_digits,
            use_special_chars=use_special_chars
        )

        if generated_password != "Please select at least one character type.":
            GeneratedPassword.objects.create(password=generated_password)
            return render(request, 'password_generator/index.html', {'generated_password': generated_password})

    return render(request, 'password_generator/index.html', {'generated_password': generated_password})