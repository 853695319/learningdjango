from django.shortcuts import render
from .models import AreaInfo


def area(request):
    _area = AreaInfo.objects.get(pk=130100)
    return render(request, 'areainfo/area.html', {'area': _area})


def ajax(requset):
    return render(requset, 'areainfo/ajax.html')


def ajax_get(request, pro_id):
    from django.http import JsonResponse

    # 获得省
    raw_list = AreaInfo.objects.filter(aparent__isnull=True)

    # QuerySet is not JSON serializable，所以要自己处理成dict格式
    data = []
    for item in raw_list:
        data.append([item.id, item.atitle])
    # 默认safe=true,只接收dict，safe=False,接收任何可JSON序列化的对象
    return JsonResponse({'data': data})
