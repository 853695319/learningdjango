from django.http import HttpResponseRedirect


def login_wrapper(func):
    """
    :param func:
    :return: func
    装饰器：登录验证，如果未登录则转到登录界面
    """
    def inner_login(request, *args, **kwargs):
        # 带参数的func inner_func也要有同样的参数
        # func(request, *args, **kwargs) -> deco(func)(request, *args, **kwargs)

        # 已经登录的用户，session会记录id
        if request.session.get('user_id', None):
            return func(request, *args, **kwargs)
        else:
            redi = HttpResponseRedirect(redirect_to='/user/login/')
            redi.set_cookie('url', request.get_full_path())
            return redi

    return inner_login


"""
http://127.0.0.1:8000/200/?type=10
request.path:表示当前路径， /200/
request.get_full_path():表示返回完整路径（但不包含域名），并包括附加的查询信息, /200/?type=10
"""