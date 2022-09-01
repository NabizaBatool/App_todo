from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import NewUserForm, TodoForm
from .models import Todo
from .task import sendmail_func


# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                form.save()
                user1 = form.cleaned_data.get('username')
                messages.success(
                    request, "Registration successful" + '' + user1)
                return redirect("loginPage")
        else:
            form = NewUserForm()
        context = {'form': form}
        return render(request, 'todo/register.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/loginpage')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect')

        return render(request, 'todo/login.html')


def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, "Task removed !!!")
    return redirect('index')


@login_required(login_url='/loginpage')
def index(request):
    list_of_tasks = Todo.objects.filter(user=request.user).order_by("-created")
    task = list_of_tasks.filter(complete=False)
    count = task.count()
    overdue_task = task.filter(created__lt=datetime.now())
    mail_subject = 'Overdue Task'
    to_email = request.user.email
    message = "These are overdue Task: "
    for i in overdue_task:
        message += ' ' + i.title
    sendmail_func.delay(mail_subject, message, to_email)
    page = {
        "list": list_of_tasks,
        "count": count
    }
    return render(request, 'todo/index.html', page)


@login_required(login_url='/loginpage')
def createTask(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('description')
        status = True if request.POST.get('complete') == 'on' else False
        date = request.POST.get('created')
        todo = Todo(user=request.user, title=title,
                    description=desc, complete=status, created=date)
        todo.save()
        messages.info(request, "Todo added")
        mail_subject = 'Create Task'
        message = "Welcome to todo app , you have created a task: " + ' ' + todo.title
        to_email = request.user.email
        sendmail_func.delay(mail_subject, message, to_email)

        return redirect('index')
    else:
        form = TodoForm()
        return render(request, 'todo/taskForm.html', {"form": form})


def update(request, item_id):
    editTask = Todo.objects.get(id=item_id)
    if request.method == "POST":
        editTask.title = request.POST.get('title')
        editTask.description = request.POST.get('description')
        if  request.POST.get('complete') == 'on':
            editTask.complete = True
            mail_subject = 'Complete Task'
            message = "Wow you have completed a task"
            to_email = request.user.email
            sendmail_func.delay(mail_subject, message, to_email)
        else:
            editTask.complete = False
        editTask.save()
        messages.info(request, "Task updated..")
        return redirect('index')
    else:
        form = TodoForm(instance=editTask)
        return render(request, 'todo/taskForm.html', {"form": form})
