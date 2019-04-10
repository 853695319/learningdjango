from django.http import HttpResponse


class MyException:
    def process_exception(request, response, exception):
        """只处理视图中的异常"""
        # exception.message 并没有这个方法！！
        return HttpResponse(exception)
