from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .form import *
from django.http import JsonResponse 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, 'welcome.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful, please log in')
        return redirect('login')
    return render(request, 'signup.html', {})

def LogoutView(request):
    logout(request)
    return redirect('welcome')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=name)
        except User.DoesNotExist:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

        validate_user = authenticate(username=user.username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html', {})

# Create your views here.
@login_required
def task_list(request):
    # Lấy nhiệm vụ chưa hoàn thành và đã hoàn thành của người dùng hiện tại
    d_tasks = Task.objects.filter(completed=False, user=request.user)
    c_tasks = Task.objects.filter(completed=True, user=request.user)
    
    # Tạo đối tượng form cho việc thêm nhiệm vụ
    form = TaskForm()
    
    if request.method == 'POST':
        if 'add_task' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                # Gán người dùng hiện tại trước khi lưu nhiệm vụ mới
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect('task_list')
        else:
            # Cập nhật nhiệm vụ
            id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=id, user=request.user)  # Đảm bảo nhiệm vụ thuộc về người dùng hiện tại
            ud = Update(request.POST, instance=task)  # Đảm bảo bạn có TaskUpdateForm
            if ud.is_valid():
                ud.save()
                return redirect('task_list')
    
    context = {
        'c_tasks': c_tasks,
        'd_tasks': d_tasks,
        'form': form
    }
    return render(request, 'task_list.html', context)

def calendar(request):
    return render(request, 'calendar.html')

def all_task(request):
    all_task = Task.objects.filter(completed = False, user=request.user)
    out = []
    for task in all_task:
        out.append({                                                                                                     
            'title': task.title,                                                                                         
            'id': task.id,                                                                                              
            'start': task.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': task.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                             
        })    
    return JsonResponse(out, safe=False) 
def add_task(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)

    if start and end and title:
        start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        task = Task(title=title, start=start, end=end)
        task.save()

    data = {}
    return JsonResponse(data)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    task = Task.objects.get(id=id)
    task.start = start
    task.end = end
    task.title = title
    task.save()
    data = {}
    return JsonResponse(data)

def remove(request):
    id = request.GET.get("id", None)
    task = Task.objects.get(id=id)
    task.delete()
    data = {}
    return JsonResponse(data)


def setting(request):
    if request.method == 'POST':
        if 'password' in request.POST:
            form = Setting(instance=request.user)
            change_password_form = ChangePasswordForm(request.user, request.POST)
            if change_password_form.is_valid():
                user = change_password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('setting')
            else:
                messages.error(request, 'Please correct the errors in the password form.')
        else:
            form = Setting(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('setting')
            else:
                messages.error(request, 'Please correct the errors in the profile form.')
        change_password_form = ChangePasswordForm(request.user)
    else:
        form = Setting(instance=request.user)
        change_password_form = ChangePasswordForm(request.user)

    return render(request, 'setting.html', {
        'form': form,
        'change_password_form': change_password_form,
    })

def pomodoro_timer(request):
    timers = Timers.objects.all().order_by('priority')
    form = PomodoroForm()
    
    if request.method == "POST":
        form = PomodoroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pomodoro_timer')

    context = {
        'form': form,
        'timers': timers,
    }
    return render(request, 'pomodoro.html', context)
