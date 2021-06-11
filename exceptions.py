# 自定义异常处理

from rest_framework.views import exception_handler
from .response import APIResponse


def common_exception_handler(exc, context):
    ret = exception_handler(exc, context)

    if not ret:
        return APIResponse(code=0, msg='error', result=str(exc))
    else:
        return APIResponse(code=0, msg='error', result=ret.data)
