from django.shortcuts import render,HttpResponse,redirect
import logging
from django.conf import settings
# 分页
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from .models import *
logger = logging.getLogger('blog.views')
from .forms import *
from django.db.models import Count
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password
# Create your views here.

def global_settings(request):

    try:
        SITE_NAME=settings.SITE_NAME
        SITE_DESC=settings.SITE_DESC
        SITE_URL = 'http://localhost:8000/'

        #广告

        #标签云

        #友情链接

        #文章排行

        #评论排行
        # comment_list=Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
        # print(len(comment_list))

        #浏览排行
        scan_list = Article.objects.all().order_by('-click_count')[0:6]

        category_list = Category.objects.all()

        article_list = Article.objects.all()

        dates = Article.objects.distinct_date()

        comment_list=Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
        print(comment_list)
        Article_comments =  (Article.objects.get(pk=comment['article']) for comment in comment_list)

    except Exception as e:
        logger.error(e)

    return locals()

def index(request):
    try:
        pass
        # category_list = Category.objects.all()
        #
        # article_list = Article.objects.all()
        #
        # dates = Article.objects.distinct_date()
        # paginator=Paginator(article_list,2)
        #
        # try:
        #     page = int(request.GET.get('page'),1)
        #     article_list = paginator.page(page)
        # except (EmptyPage,InvalidPage,PageNotAnInteger):
        #     article_list = paginator.page(1)

    except Exception as e:
        logger.error(e)

    return render(request,'left_content.html',locals())

def achieve(request):
    try:


        # 获取客户端提交信息
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)
        day = request.GET.get('day',None)

        # 模糊查询
        article_list = Article.objects.filter(date_publish__icontains = year +'-'+ month +'-'+ day)


    except Exception as e:
        logger.error(e)

    return render(request,'achieve.html',locals())

def article(request):

    id = request.GET.get('id')

    try:
        article = Article.objects.get(pk=id)


    # except Article.DoesNotExist:
    #     return HttpResponse('没有找到相关文章')

        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_len = len(comments)

        # 父级评论
        comment_list = []
        comment_sublist=[]
        # 遍历所有评论
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
                for sub_comment in comment_list:
                    if sub_comment.pid == item:
                        item.children_comment.append(sub_comment)
                        comment_sublist.remove(sub_comment)
            if comment.pid is None:
                comment_list.append(comment)
            if comment.pid is not None:
                comment_sublist.append(comment)

        # 显示评论表单
        comment_form = CommentForm({'author':request.user.username,
                                    'email':request.user.email,
                                    'url':request.user.url,
                                    'articla':id
                                    } if request.user.is_authenticated() else {'article':id})
    except Exception as e:
        print(e)
        logger.error(e)


    return render(request,'article.html',locals())

# 提交评论
def comment_post(request):

    try:
        comment_form = CommentForm(request.POST)
        hidden_id = request.POST.get('hidden_id')

        print(comment_form)
        print (str(comment_form.is_valid()))

        if comment_form.is_valid():
            # 获取表单信息 并保存到数据库
            comment = Comment.objects.create(username=comment_form.cleaned_data['author'],
                                             email = comment_form.cleaned_data['email'],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=hidden_id,
                                             user =request.user if request.user.is_authenticated() else None
                                             )
            comment.save()
            print('v 保存成功～～～～～～～～～～～～～～·')
        else:
            return HttpResponse('出错了！！！')
    except Exception as e:
        print('出错了～～～～～～～～～～～～～～～～～～～～～')
        print(e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e :
        print(e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(username=reg_form.cleaned_data['username'],
                                           email=reg_form.cleaned_data['email'],
                                           password=make_password(reg_form.cleaned_data['password']),
                                           url=reg_form.cleaned_data['url']
                                           )
                user.save()

                # 注册完毕后自动登陆

                #制定默认的登陆验证方式
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                return redirect(request.POST.get('source_url'))
            else:
                return HttpResponse(reg_form.errors)
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request,'reg.html',locals())

def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return HttpResponse('表单验证不合格')
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())