from django.shortcuts import render
from django.http import JsonResponse
from .models import AreaInfo


def area(request):
    _area = AreaInfo.objects.get(pk=130100)
    return render(request, 'areainfo/area.html', {'area': _area})


def ajax(requset):
    return render(requset, 'areainfo/ajax.html')


def ajax_get_pro(request):
    # http://127.0.0.1:8000/area-pro/

    # 获得省
    pro_list = AreaInfo.objects.filter(aparent__isnull=True)

    # QuerySet is not JSON serializable，所以要自己处理成dict格式
    data = []
    for pro in pro_list:
        data.append([pro.id, pro.atitle])
    # 默认safe=true,只接收dict，safe=False,接收任何可JSON序列化的对象
    return JsonResponse({'data': data})  # {'data':[[110000, '北京市'], [], []]}


def ajax_get_city(request, pro_id):
    # http://127.0.0.1:8000/area-city-140000/

    # 根据省的id获得它的下属city
    # 1 aparent_id == 关联的上级areainfo.id 去数据库看看
    # city_list = AreaInfo.objects.filter(aparent_id=pro_id)
    # 2 利用定义模型章节讲到的关系
    pro = AreaInfo.objects.get(id=pro_id)  # 省
    city_list = pro.areainfo_set.all()  # 市 省关联的下属城市
    data = []
    for city in city_list:
        data.append({'id': city.id, 'title': city.atitle})
    return JsonResponse({'data': data})  # {'data': [{}, {}, {}]}
