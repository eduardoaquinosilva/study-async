from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Workbook, WorkbookView
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def add_workbooks(request):
    if request.method == "GET":
        workbooks = Workbook.objects.filter(user=request.user)
        total_views = WorkbookView.objects.filter(workbook__user=request.user).count()

        return render(request, 'add_workbook.html', {'workbooks': workbooks, 'total_views': total_views})

    if request.method == "POST":
        title = request.POST.get('title')
        file = request.FILES['file']

        workbook = Workbook(user=request.user, title=title, file=file)
        workbook.save()

        messages.add_message(request, constants.SUCCESS, 'Salvo com sucesso.')
        return redirect(reverse('add_workbooks'))

def workbook(request, id):
    if request.method == "GET":
        workbook = Workbook.objects.get(id=id)
        
        view = WorkbookView(ip=request.META['REMOTE_ADDR'], workbook=workbook)
        view.save()

        total_views = WorkbookView.objects.filter(workbook=workbook).count()
        unique_views = WorkbookView.objects.filter(workbook=workbook).values('ip').distinct().count()

        return render(request, 'workbook.html', {'workbook': workbook, 'total_views': total_views, 'unique_views': unique_views})
