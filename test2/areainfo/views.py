from django.shortcuts import render
from .models import AreaInfo


def area(request):
    _area = AreaInfo.objects.get(pk=130100)
    return render(request, 'areainfo/area.html', {'area': _area})
