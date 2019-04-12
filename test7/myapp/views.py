from django.shortcuts import render
from .models import Note

# 全文检索
def mysearch(request):
    return render(request, 'myapp/mysearch.html')

