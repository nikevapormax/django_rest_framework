from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Article as ArticleModel
from .models import Comment as CommentModel

from datetime import datetime

from django_rest_framework.permissions import MyAuthenticateOver3, IsAdminOrIsAuthenticated

class ArticleView(APIView):
    
    permission_classes = [IsAdminOrIsAuthenticated]
    
    def get(self, request):      
        user = request.user
        # articles = ArticleModel.objects.filter(author=user)
        
        today = datetime.now()
        time = ArticleModel.objects.filter(exposure_start__lte=today, exposure_end__gte=today).order_by("-exposure_start")
        if time:
            show_article = [f'{article.title} : {article.content}' for article in time]

            return Response({"articles": show_article})
        return Response({"msg": "노출기간에 해당하는 게시글이 없습니다."})

    def post(self, request):
        user = request.user
        title = request.data.get('title', '')
        content = request.data.get('content', '')
        categorys = request.data.get('category', [])
        
        
        if len(title) <= 5:
            return Response({"error": "제목은 5자보다 많아야 합니다."})
        if len(content) <= 20:
            return Response({"error": "게시글은 20자보다 많아야 합니다."})
        if not categorys:
            return Response({"error": "카테고리가 지정되지 않았습니다."})
        
        article = ArticleModel(author=user, title=title, content=content)
        article.save()
        article.category.add(*categorys)

        return Response({"msg": "게시글 작성 성공!!"}, status=status.HTTP_200_OK)
    