from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from Blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),  # 首页
    path('list-<int:lid>.html', views.list, name='list'),  # 列表页
    path('show-<int:sid>.html', views.show, name='show'),  # 内容页
    path('tag/<tag>', views.tag, name='tags'),  # 标签列表页
    path('s/', views.search, name='search'),  # 搜索列表页
    path('about/', views.about, name='about'),  # 联系我们单页
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
