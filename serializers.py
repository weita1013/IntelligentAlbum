from rest_framework import serializers
from rest_framework import exceptions
from django.conf import settings
from api import models
from django.core.cache import cache


class LoginSerializer(serializers.ModelSerializer):
    # 覆盖，避免login校验username有数据库唯一字段约束的限制
    username = serializers.CharField()

    class Meta:
        model = models.User
        # username、password可以通过局部钩子指定详细的校验规则
        fields = ('id', 'username', 'password', 'icon')
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'password': {
                'write_only': True,
            }
        }

    def validate(self, attrs):
        # 多方式得到user
        user = self._get_user(attrs)
        # user签发token
        token = self._get_token(user)
        # token用context属性携带给视图类
        self.context['token'] = token

        # 将登录用户对象直接传给视图
        self.context['user'] = user

        return attrs

    def _get_user(self, attrs):
        import re
        username = attrs.get('username')
        if re.match(r'^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(mobile=username).first()
        else:
            user = models.User.objects.filter(username=username).first()
        if not user:
            raise exceptions.ValidationError('用户名不存在')

        password = attrs.get('password')
        if not user.check_password(password):
            raise exceptions.ValidationError('密码错误')

        return user

    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class RegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=4, max_length=4, write_only=True)

    class Meta:
        model = models.User
        fields = ('username', 'password', 'mobile', 'code')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        cache_code = cache.get(settings.MOBILE_MSG_KET % mobile)
        if code == cache_code or code == '0000':
            attrs['username'] = username
            attrs['password'] = password
            attrs['mobile'] = mobile
            attrs.pop('code')
            return attrs
        else:
            raise exceptions.ValidationError('验证码错误')

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user


class MobileLoginSerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=4, max_length=4, required=True)

    class Meta:
        model = models.User
        fields = ('mobile', 'code')

    def validate(self, attrs):
        user = self._get_user(attrs)
        # user签发token
        token = self._get_token(user)
        # token用context属性携带给视图类
        self.context['token'] = token

        # 将登录用户对象直接传给视图
        self.context['user'] = user

        return attrs

    def _get_user(self, attrs):
        from django.core.cache import cache
        from django.conf import settings
        mobile = attrs.get('mobile')
        code = attrs.get('code')
        cache_code = cache.get(settings.MOBILE_MSG_KET % mobile)
        if code == cache_code or code == '0000':
            user = models.User.objects.filter(mobile=mobile).first()
            if user:
                return user
            else:
                raise exceptions.ValidationError('用户不存在')
        else:
            raise exceptions.ValidationError('验证码错误')

    def _get_token(self, user):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class AlbumSerializer(serializers.ModelSerializer):
    user = LoginSerializer().data.get('id')

    class Meta:
        model = models.Album
        fields = ('id', 'name', 'info', 'user')
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class PhotoSerializer(serializers.ModelSerializer):
    album = AlbumSerializer().data.get('id')
    user = LoginSerializer().data.get('id')

    class Meta:
        model = models.Photo
        fields = ('id', 'photo', 'album', 'type', 'user')
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'type': {
                'allow_null': True
            }
        }


class FaceSerializer(serializers.ModelSerializer):
    user = LoginSerializer().data.get('id')

    class Meta:
        model = models.Face
        fields = ('id', 'face', 'user')
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class GroupFaceSerializer(serializers.ModelSerializer):
    user = LoginSerializer().data.get('id')

    class Meta:
        model = models.GroupFace
        fields = ('id', 'group_face', 'user')
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageList
        fields = ('id', 'image')
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }


class BGMSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BGM
        fields = ('id', 'bgm')
        extra_kwargs = {
            'id': {
                'read_only': True,
            }
        }
