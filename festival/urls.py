from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('gallery', views.start_page, name='start_page_redirect'),
    path('gallery/images', views.images_festival_page, name='images_festival_page'),
    path('gallery/stories', views.stories_festival_page, name='stories_festival_page'),
    path('gallery/add_comment/<str:TYPE>_<int:ID>', views.new_comment_page,
         name='images_new_comment'),
    path('gallery/view_comments/<str:TYPE>_<int:ID>', views.view_comments_page,
         name='images_new_comment')
]
