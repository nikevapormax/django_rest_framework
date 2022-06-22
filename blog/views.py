from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Article as ArticleModel
from .models import Comment as CommentModel
from .serializers import ArticleSerializer

from datetime import datetime

from django_rest_framework.permissions import MyAuthenticateOver3, IsAdminOrIsAuthenticated

class ArticleView(APIView):
    
    permission_classes = [IsAdminOrIsAuthenticated]
    
    def get(self, request):      
        user = request.user
        # articles = ArticleModel.objects.filter(author=user)
        
        today = datetime.now()
        time = ArticleModel.objects.filter(exposure_start__lte=today, exposure_end__gte=today).order_by("-id")
        # if time:
        #     show_article = [f'{article.title} : {article.content}' for article in time]

        #     return Response({"articles": show_article})
        # return Response({"msg": "노출기간에 해당하는 게시글이 없습니다."})
        return Response(ArticleSerializer(time, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        request.data['author'] = user.id
        article_serializer = ArticleSerializer(data=request.data)
        
        # request.data의 유효성 검증
        if article_serializer.is_valid():  # True or False로 결과값이 나옴
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        
        # False인 경우 어디서 에러가 났는지 보여줌
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # title = request.data.get('title', '')
        # content = request.data.get('content', '')
        # categorys = request.data.get('category', [])
        
        
        # if len(title) <= 5:
        #     return Response({"error": "제목은 5자보다 많아야 합니다."})
        # if len(content) <= 20:
        #     return Response({"error": "게시글은 20자보다 많아야 합니다."})
        # if not categorys:
        #     return Response({"error": "카테고리가 지정되지 않았습니다."})
        
        # article = ArticleModel(author=user, title=title, content=content)
        # article.save()
        # article.category.add(*categorys)

        # return Response({"msg": "게시글 작성 성공!!"}, status=status.HTTP_200_OK)
    