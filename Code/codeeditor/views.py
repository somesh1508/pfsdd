from openai import OpenAI
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import UserCode
import subprocess

client = OpenAI(api_key=settings.OPENAI_API_KEY)
def logout_view(request):
    logout(request)
    return redirect('home')
def get_ai_suggestion(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        # Get AI suggestions for the code
        if code.strip():
            try:
                ai_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"Provide suggestions for this {language} code:\n{code}"}],
                    max_tokens=150
                )
                ai_suggestion = ai_response.choices[0].message.content
            except Exception as e:
                ai_suggestion = f"Error getting AI suggestion: {str(e)}"

        return JsonResponse({'ai_suggestion': ai_suggestion})
    return JsonResponse({'error': 'Invalid request'}, status=400)



def home(request):
    return render(request, 'home.html')

from django.contrib.auth import logout
from django.shortcuts import redirect, render

def user_logout(request):
    logout(request)  # Log the user out
    return redirect('logout_successful')  # Redirect to the logout success page


def logout_successful(request):
    return render(request, 'logout_successful.html')  # Replace with your actual template path

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Ensure 'login' is the correct URL name
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Get the next parameter for redirection
                next_url = request.GET.get('next', 'editor')  # Default to 'editor'
                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def code_editor(request):
    output = ''
    languages = ['Python', 'JavaScript', 'Java', 'C++']  # Include Java

    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        user_input = request.POST.get('user_input')  # Get user input

        # Save code to the database
        user_code = UserCode(user=request.user, language=language, code=code)
        user_code.save()

        # Execute the code based on the selected language
        try:
            if language == 'Python':
                with open('temp_code.py', 'w') as f:
                    f.write(code)
                result = subprocess.run(['python3', 'temp_code.py'], input=user_input, text=True, capture_output=True)
                output = result.stdout + result.stderr

            elif language == 'JavaScript':
                with open('temp_code.js', 'w') as f:
                    f.write(code)
                result = subprocess.run(['node', 'temp_code.js'], input=user_input, text=True, capture_output=True)
                output = result.stdout + result.stderr

            elif language == 'Java':
                with open('temp_code.java', 'w') as f:  # Correctly save as .java
                    f.write(code)
                compile_result = subprocess.run(['javac', 'temp_code.java'], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    output = compile_result.stderr
                else:
                    run_result = subprocess.run(['java', 'temp_code'], input=user_input, text=True, capture_output=True)
                    output = run_result.stdout + run_result.stderr

            elif language == 'C++':
                with open('temp_code.cpp', 'w') as f:
                    f.write(code)
                compile_result = subprocess.run(['g++', 'temp_code.cpp', '-o', 'temp_code'], capture_output=True, text=True)
                if compile_result.returncode != 0:
                    output = compile_result.stderr
                else:
                    run_result = subprocess.run(['./temp_code'], input=user_input, text=True, capture_output=True)
                    output = run_result.stdout + run_result.stderr

            # Save output
            user_code.output = output
            user_code.save()

        except Exception as e:
            output = f"Error executing code: {str(e)}"

        return JsonResponse({'output': output})

    return render(request, 'codeeditor/editor.html', {'languages': languages})



@login_required
def about(request):
    return render(request, 'codeeditor/about.html')

def login_view(request):
    return render(request, 'login.html')  # Replace 'login.html' with the correct template path
