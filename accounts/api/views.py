from accounts.api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)
from accounts.api.serializers import SignupSerializer, LoginSerializer


#modelviewset is native one from django framework
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined') # select * from user order by date_join desc
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # any operation needs authentication


class AccountViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        """
        默认的 username 是 admin, password 也是 admin
        """
        #get post request body
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django_authenticate(username=username, password=password)
        #User.objects.filter(username=username) will be translated to a query
        #you can debug by
        # queryset = User.objects.filter(username=username)
        # print(queryset.query)
        if not User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "Please check input."
            }, status=400)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "Username and password does not match.",
            }, status=400)
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        })

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        """
        登出当前用户
        """
        django_logout(request)
        return Response({"success": True})

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        """
        使用 username, email, password 进行注册
        """
        # 不太优雅的写法
        # username = request.data.get('username')
        # if not username:
        #     return Response("username required", status=400)
        # password = request.data.get('password')
        # if not password:
        #     return Response("password required", status=400)
        # if User.objects.filter(username=username).exists():
        #     return Response("password required", status=400)
        serializer = SignupSerializer(data=request.data)
        # is_valid will trigger serializer.valide() method check
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        #save will create the user row or update it
        user = serializer.save()
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        })

    @action(methods=['GET'], detail= False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)