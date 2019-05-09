from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry
from .forms import ArticleForm
from django.utils.http import quote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.utils.http import quote_plus

# Create your views here.

def articles(request):
    todayDate=timezone.now().date()
    article_list=Entry.objects.active().order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        article_list=Entry.objects.all()

    #searches through the post
    query=request.GET.get("quote")
    if query:
        article_list=article_list.filter(
            Q(title__icontains=query)| 
            Q(body__icontains=query)| 
            Q(authors__name__icontains=query)
            ).distinct()

    #this manages the pagination
    paginator= Paginator(article_list, 12)
    page_request_var="page"
    page=request.GET.get(page_request_var)
    try:
        queryset=paginator.get_page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context={
    "today": todayDate,
    "article_list":article_list,
    "page_request_var":page_request_var,
     "object_list":queryset,
    }
    return render(request, 'articles/articles.html', context)


def create_article(request):
    #checks the users level
    form=ArticleForm(request.POST or None)
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if form.is_valid():
        instance=form.save(commit=False)#confirms the goodness of the data
        instance.user=request.user#bring forth the logged-in user
        instance.save()#saves the data into the database
        messages.success(request, "Created Successfully")
        return HttpResponseRedirect(instance.get_absolute_url())
    article_form = {"form": form, }
    return render(request, "articles/create_article.html", article_form)

def article_details(request, slug):
        articles=Entry.objects.get(slug=slug)
        return render(request, 'articles/articles_details.html', {'fullarticle':articles})

def articles_update(request, slug=None):
    # checks the users level
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    articleUpdater=get_object_or_404(Entry, slug=slug)
    form = ArticleForm(request.POST or None,request.FILES or None, instance=articleUpdater)
    if form.is_valid():
        articleUpdater = form.save(commit=False)  # confirms the goodness of the data
        articleUpdater.save()  # saves the data into the database
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(articleUpdater.get_absolute_url())#redirects after Successfully sent to DB
    context ={"title":articleUpdater.title, "instance":articleUpdater, "form":form}

    return render(request, 'articles/create_article.html', context)

def delete_article(request, slug=None):
    # checks the users level
    if not request.user.is_superuser:
        messages.success(request, "<h2>Sorry cannot find the page you are looking for</h2>", extra_tags='html_safe')
        return redirect("articles:list")
    getter=get_object_or_404(Entry, slug=slug)
    getter.delete()
    messages.success(request, "Deleted Successfully")
    return redirect("articles:list")
