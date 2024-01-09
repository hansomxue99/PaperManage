from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PaperInfo
import markdown
from .forms import PaperInfoForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


# 视图函数
def article_list(request):
    search = request.GET.get('search')
    tag = request.GET.get('tag')

    articles_list = PaperInfo.objects.all()

    if search:
        articles_list = articles_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 标签查询集
    if tag and tag != 'None':
        articles_list = articles_list.filter(tags__name__in=[tag])

    paginator = Paginator(articles_list, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'articles': articles,
        'search': search,
        'tag': tag,
    }
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = PaperInfo.objects.get(id=id)
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == "POST":
        article_post_form = PaperInfoForm(data=request.POST)
        print(article_post_form)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = PaperInfoForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = PaperInfo.objects.get(id=id)
        if request.user.username != article.author:
            return HttpResponse("抱歉，你无权删除这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = PaperInfo.objects.get(id=id)
    if request.user.username != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == "POST":
        article_post_form = PaperInfoForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.paper_author = request.POST['paper_author']
            article.source = request.POST['source']
            article.reference = request.POST['reference']
            article.tags.set(request.POST.get('tags').split(','), clear=True)
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    else:
        article_post_form = PaperInfoForm()
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
