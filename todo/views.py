from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import NewUserForm, TodoForm
from .models import Todo
from .task import sendmail_func


# Create your views here.
#
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
    list = Todo.objects.filter(user=request.user).order_by("-created")
    count = list.count()-list.all().filter(complete=True).count()
    completed = Todo.objects.filter(user=request.user, complete=True)
   # print(completed)
    # print(date.today())
  #  print(list[0].created.date())
    task = Todo.objects.filter(user=request.user, complete=False)
    print(task)
    overdue = []
    for task in task:

        if task.created.date() < date.today():
            overdue.append(task)

        else:
            continue
    print("overdue check")
    print(overdue)

    mail_subject = 'Overdue Task'
    to_email = request.user.email
    message = "These are overdue Task: "
    for i in overdue:
        message += ' ' + i.title
        print(message)

    sendmail_func.delay(mail_subject, message, to_email)

    page = {
        "list": list,
        "count": count
    }
    return render(request, 'todo/index.html', page)


@login_required(login_url='/loginpage')
def createTask(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('description')
        status = request.POST.get('complete')
        if status == 'on':
            status = True
        else:
            status = False
        date = request.POST.get('created')
        todo = Todo(user=request.user, title=title,
                    description=desc, complete=status, created=date)
        todo.save()
        messages.info(request, "Todo added")
        mail_subject = 'Create Task'
        message = "Welcome to todo app , you have created a task"
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
        editTask.complete = request.POST.get('complete')
        if editTask.complete == 'on':
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
