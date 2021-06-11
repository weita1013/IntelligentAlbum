# 自定义response

from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, code=1, msg='成功', result=None, status=None, headers=None, **kwargs):
        dic = {'code': code, 'msg': msg}
        if result:
            dic = {'code': code, 'msg': msg, 'data': result}
        dic.update(kwargs)
        super().__init__(data=dic, status=status, headers=headers)
