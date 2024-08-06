from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from .form import *
from django.http import JsonResponse 

def welcome (request):
    return render(request, 'welcome.html')
def signup (request):
    return render(request, 'signup.html')
def loginpage(request):
    return render(request, 'login.html')

# Create your views here.
def task_list(request):
    d_tasks = Task.objects.filter(completed=False)
    c_tasks = Task.objects.filter(completed=True)
    form = TaskForm()
    if request.method=='POST':
        if 'add_task' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid(): 
                form.save()
                return redirect('task_list')
        else:
            id = request.POST.get('task_id')
            task = get_object_or_404(Task,id = id)
            ud = Update(request.POST, instance = task)
            if ud.is_valid():
                ud.save()
                return redirect('task_list')
    context = {
        'c_tasks':c_tasks,
        'd_tasks':d_tasks,
        'form':form
    }
    return render(request,'task_list.html',context)

def calendar(request):
    return render(request, 'calendar.html')

def all_task(request):
    all_task = Task.objects.filter(completed = False)
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
        form = Setting(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('setting') 
    else:
        form = Setting(instance=request.user)

    return render(request, 'setting.html', {'form': form})