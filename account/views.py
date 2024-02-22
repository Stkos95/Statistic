from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse

from .forms import CustomUserCreationForm



# def login_view(request, *args, **kwargs):
#     if request.method.lower() == 'post':
#         print('here')
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if user:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     return HttpResponse('disabled account')
#             else:
#                 return HttpResponse('invalid account')
#         else:
#             print(form.errors)
#             return render(request, 'registration/login.html', {'form': form})
#     form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})




def registration_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            new_user = form.save(commit=False)
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            return redirect('statistic:initial')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})

def change_password_view(request, *args, **kwargs):
    user = request.user
    if request.method.lower() == 'post':
        user = request.user
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registration/password_change_done.html', {})
    else:
        form = PasswordChangeForm(user)
    return render(request, 'registration/password_change_form.html', {'form': form})

def reset_password_view(request, *args, **kwargs):
    if request.method.lower() == 'post':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', None)
            if email:
                form.save(
                    subject_template_name='registration/password_reset_subject.txt',
                    email_template_name='registration/password_reset_email.html',
                    from_email='admin@plstkos.site',
                    request=request
                )
                return HttpResponse('sent')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})




