from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
import openai

openai_api_key = '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'

openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150,
        n = 1,
        stop = None,
        temperature = 0.7
    )

    answer = response.choices[0].text.strip()
    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Something went wrong'
                return render(request, 'register.html', {'error_message': error_message })
        else:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)