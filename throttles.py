from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache
from django.conf import settings


class SMSRateThrottle(SimpleRateThrottle):
    scope = 'sms'

    def get_cache_key(self, request, view):
        # 对手机号频率限制
        mobile = request.query_params.get('mobile', None)
        if not mobile:  # 为发现限制条件，返回None代表不进行频率限制
            return None
        code = cache.get(settings.MOBILE_MSG_KET % mobile)
        if not code:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': mobile
        }
