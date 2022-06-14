from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
import bcrypt

def login_reg(request):
    return render(request, "login_reg.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
        request.session['user_id'] = new_user.id
        return redirect('/landing')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = this_user.id
        return redirect('/landing')
    return redirect('/')


def landing(request):
    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'current_user': current_user,
    }
    return render(request, 'landing.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def create_entry(request):
    if request.method == "POST":
        entry_text = request.POST['entry_text']
        entry_title = request.POST['entry_title']
        author = User.objects.get(id = request.session['user_id'])
        new_entry = Entry.objects.create(entry_text = entry_text, author = author, title = entry_title)
        return redirect(f'/my_entries/{author.id}')
    return redirect('/landing')

def my_entries(request, current_user_id):
    current_user = User.objects.get(id = current_user_id)
    current_user_entries = current_user.entries.all().order_by('-created_at')
    paginator = Paginator(current_user_entries, 10)
    page = request.GET.get('page')
    try: 
        current_user_entries = paginator.page(page)
    except PageNotAnInteger:
        current_user_entries = paginator.page(1)
    except EmptyPage:
        current_user_entries = paginator.page(paginator.num_pages)
    context = {
        'current_user_entries': current_user_entries,
        'current_user': current_user,
        'page': page
    }
    return render(request, 'user_entries.html', context)

def view_entry(request, entry_id):
    current_entry = Entry.objects.get(id = entry_id)
    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'current_entry': current_entry,
        'current_user': current_user
    }
    return render(request, 'entry.html', context)

def delete(request, entry_id):
    current_entry = Entry.objects.get(id = entry_id)
    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'current_entry': current_entry,
        'current_user': current_user
    }
    return render(request,'confirm_delete.html', context)

def delete_entry(request, entry_id):
    current_user = User.objects.get(id = request.session['user_id'])
    current_user_entries = current_user.entries.all()
    entry_to_delete = Entry.objects.get(id = entry_id)
    entry_to_delete.delete()
    context = {
        'current_user_entries': current_user_entries,
        'current_user': current_user
    }
    return redirect(f'/my_entries/{current_user.id}', context)

def edit_entry(request, entry_id):
    entry_to_edit = Entry.objects.get(id = entry_id)
    entry_to_edit.entry_text = request.POST['entry_text']
    entry_to_edit.title = request.POST['entry_title']
    entry_to_edit.save()
    current_entry = Entry.objects.get(id = entry_id)
    current_user = User.objects.get(id = request.session['user_id'])
    context = {
        'current_entry': current_entry,
        'current_user': current_user
    }
    return redirect(f'/my_entries/{current_user.id}', context)

def edit_user_info(request, current_user_id):
    current_user = User.objects.get(id = current_user_id)
    context = {
        'current_user': current_user
    }
    return render(request, 'edit_user_info.html', context)

def edit_user_info_complete(request, current_user_id):
    if request.method == 'POST':
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit_user_info/{current_user_id}')
        user_to_update = User.objects.get(id = current_user_id)
        user_to_update.first_name = request.POST['first_name']
        user_to_update.last_name = request.POST['last_name']
        user_to_update.email = request.POST['email']
        user_to_update.save()
        return redirect('/landing')
    return redirect('/landing')
