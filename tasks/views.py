# vies handle request and return responses

from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

# List all tasks anyone can view


def task_list(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "tasks/task_list.html", {"tasks": tasks})


# view task details
def task_details(request, pk):
    task = get_list_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


# create task only for logged-in users
@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect(task_list)
        else:
            form = TaskForm()
            return render(request, "task/task_form.html", {"form": form})

        # Update tasks(only loggin-in users who own the task)!
        @login_required
        def task_update(request, pk):
            task = get_list_or_404(task, pk=pk)
            if task.created_by != request.user:
                return redirect("task_list")

            if request.method == "POST":
                form = TaskForm(request.POST, instance=task)
                if form.is_valid():
                    form.save()
                    return redirect("task_detail", pk=task.pk)
                else:
                    form = TaskForm(instance=task)
                    return render(request, "tasks/task_form.html", {"form": form})
                
                #Delete tasks(Only logged-in users who own the tasks)
@login_required
def task_delelte(request, pk):
    task = get_list_or_404(Task, pk=pk)
    if task.created_by != request.user:
        return redirect('task_list')
    
    if request.method =='POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html',{'task':task})