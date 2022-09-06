from django.urls import path

# Импортируем созданное нами представление
from .views import PostList, PostDetail, NewsCreate, ArticleCreate, ArticleUpdate, NewsUpdate, ArticleDelete, NewsDelete

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]
