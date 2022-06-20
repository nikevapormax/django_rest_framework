from rest_framework.permissions import BasePermission
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status


class MyAuthenticateOver3(BasePermission):
    
    message = "가입 후 3일이 지나지 않아 글 작성이 불가능합니다."
    
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        # DateField : 2022-06-18
        # DataTimeField : 2022-06-18 10:50:55
        # datetime.now().date() 를 통해서 시간까지는 안나오게 설정함
        
        print(f'user join date : {user.join_data}')
        print(f'now date : {timezone.now()}')
        print(f'a week ago date : {timezone.now() - timedelta(minutes=3)}')
        
        return bool(user.join_data < (timezone.now() - timedelta(minutes=3)))
    
    
class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrIsAuthenticated(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회는 가능하지만 게시글 작성은 일주일이 지나야 가능
    """
    SAFE_METHODS = ('POST', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        
        if user.is_authenticated and request.method == 'GET':
            return True

        # 유저가 인증되어있고 어드민이라면 전부다 할 수 있다.
        if user.is_authenticated and user.is_admin:
            return True
        
        # 유저가 인증되어있고, 가입한지 일주일이 넘었다면 트루(어드민 아닌 사람들)
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            print(bool(user.join_data < timezone.now() - timedelta(days=7)))
            return bool(user.join_data < timezone.now() - timedelta(days=7))

        return False
    
# class IsAdminOrIsAuthenticatedPost(BasePermission):
#     """
#     admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
#     """
#     SAFE_METHODS = ('POST', )
#     message = '접근 권한이 없습니다.'

#     def has_permission(self, request, view):
#         user = request.user

#         if not user.is_authenticated:
#             response ={
#                     "detail": "서비스를 이용하기 위해 로그인 해주세요.",
#                 }
#             raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        

#         # 유저가 인증되어있고 어드민이라면 전부다 할 수 있다.
#         if user.is_authenticated and user.is_admin:
#             return True
        
#         # 유저가 인증되어있고, 가입한지 일주일이 넘었다면 트루(어드민 아닌 사람들)
#         if user.is_authenticated and request.method in self.SAFE_METHODS:      
#             print(bool(user.join_data < timezone.now() - timedelta(days=7)))
#             return bool(user.join_data < timezone.now() - timedelta(days=7))

#         return False