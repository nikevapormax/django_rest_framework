from django.contrib import admin
from .models import Category as CategoryModel, Article as ArticleModel
from .models import Comment as CommentModel

# Register your models here.
admin.site.register(ArticleModel)
admin.site.register(CategoryModel)
admin.site.register(CommentModel)