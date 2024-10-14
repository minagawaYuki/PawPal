from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .forms import UpdateProfileForm

# Create your views here.
@login_required
def user_profile(request):
    users = User.objects.all()
    user = request.user
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user_id = user.id
            user = User.objects.get(id=user_id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user.save()
            return render(request, 'userprofile/user_profile.html', {'users': users, 'form': form, 'user': user})
    else:
        form = UpdateProfileForm()
        form.fields['first_name'].initial = user.first_name
        form.fields['last_name'].initial = user.last_name
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        form.fields['password'].initial = user.password
    return render(request, 'userprofile/user_profile.html', {'users': users, 'form': form, 'user': user})
