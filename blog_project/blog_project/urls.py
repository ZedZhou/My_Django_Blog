"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog_app01 import views

from django.conf import settings
from blog_app01.upload_img import upload_image


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),
    # 文件上传
    url(r"^upload/(?P<path>.*)$",\
        "django.views.static.serve",\
        {'document_root':settings.MEDIA_ROOT}),

    # 文件上传
    url(r'^admin/upload/(?P<dir_name>[^/]+)$',upload_image,name='upload_image'),

    # 文章存档（按照 日）
    url(r'^achieve/$',views.achieve,name='achieve'),
    # 显示某一文章详情
    url(r'^article/$',views.article,name='article'),
    # 提交评论
    url(r'^comment/post/$',views.comment_post,name='comment_post'),
    url(r'^logout/$',views.do_logout,name='logout'),
    url(r'^login/$',views.do_login,name='do_login'),
    url(r'^reg/$',views.do_reg,name='do_reg'),
]
