from django.db.models import Q
from django.shortcuts import render
from Blog.models import Article, Category, Banner, Tag, Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown


def global_variable(request):
    name = Category.objects.all()
    remen = Article.objects.filter(tui_id=3)[:6]
    tags = Tag.objects.all()
    return locals()


def index(request):
    article = Article.objects.all().order_by('-id')[0:10]
    tui = Article.objects.filter(tui_id=2)[:3]
    ban = Banner.objects.filter(is_active=True)[0:4]
    hot = Article.objects.all().order_by('views')[:10]
    link = Link.objects.all()
    return render(request, 'index.html', locals())


def list(request, lid):
    list = Article.objects.filter(category_id=lid)  # 获取URL传进来的lid
    cname = Category.objects.get(id=lid)  # 获取当前文章的栏目名
    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list, 2)  # 对查询到的数据对象list进行分页，超过5条就分页
    try:
        list = paginator.page(page)  # 获得当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的不是整数时，显示第一页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页码不是系统页码列表中时，显示最后一页
    return render(request, 'list.html', locals())  # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典


def show(request, sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    allcategory = Category.objects.all()  # 导航上的分类
    hot = Article.objects.all().order_by('?')[:10]  # 随机推荐
    show.body = markdown.markdown(show.body,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    precious_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    next_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    page = request.GET.get('page')
    list = show.body
    paginator = Paginator(list, 2000)  # 超过2000字就分页
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'show.html', locals())


def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)  # 通过筛选标签查找对于的文章
    tname = Tag.objects.get(name=tag)
    page = request.GET.get('page')
    paginator = Paginator(list,2)  # 超过2条就分页
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request,'tags.html',locals())


def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键字
    list = Article.objects.filter(Q(title__icontains=ss)|Q(body__icontains=ss))  # 将获取的关键字在数据库中匹配筛选,icontains是忽略大小写，contains是精确查找，区分大小写
    page = request.GET.get('page')
    paginator = Paginator(list, 2)
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'search.html', locals())


def about(request):
    allcategory = Category.objects.all()
    return render(request, 'page.html', locals())
