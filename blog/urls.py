from django.urls import path
from .views import * # ShowAllView, ArticleView, RandomArticleView # our view class definition 
from django.contrib.auth import views as auth_views

urlpatterns = [
    # map the URL (empty string) to the view
    path('', RandomArticleView.as_view(), name='random'), 
    path('show_all', ShowAllView.as_view(), name='show_all'), 
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new
    path('article/<int:pk>', ArticleView.as_view(), name='article'), # show one article ### NEW
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), ### NEW
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"), # NEW
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),  ## NEW
    # authentication views
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
    path('register/', RegistrationView.as_view(), name='register'),
]