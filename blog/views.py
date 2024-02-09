from django.shortcuts import render, redirect, HttpResponse
from . models import *
from . form import CustomUserFrom
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    posts = Article.objects.filter(featured=True).order_by('-date')

    items_per_page = 2
    paginator = Paginator(posts, items_per_page)
    page = request.GET.get('page')
    try:
        # Get the Page object for the current page
        current_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        current_page = paginator.page(paginator.num_pages)
    current_page_data = current_page.object_list

    return render(request, 'blog/pages/index.html', {'current_page_data': current_page_data, 'paginator': paginator, 'current_page': current_page, })


def topicspage(request):
    topics = Category.objects.filter(status=0)
    return render(request, 'blog/pages/topics.html', {'topics': topics})


def topicarticlepage(request, name):

    if (Category.objects.filter(name=name, status=0)):
        topicarticle = Article.objects.filter(
            catregory__name=name).order_by('-date')
        # queryset = Article.objects.all()
        items_per_page = 4
        paginator = Paginator(topicarticle, items_per_page)
        page = request.GET.get('page')
        try:
            # Get the Page object for the current page
            current_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            current_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver the last page
            current_page = paginator.page(paginator.num_pages)
        current_page_data = current_page.object_list
        return render(request, 'blog/pages/topicarticles.html', {'topicarticle': topicarticle, 'category': name,  'paginator': paginator, 'current_page': current_page, 'current_page_data': current_page_data})
    else:
        messages.warning(request, 'no such topics')
        return redirect('/')


def registerpage(request):
    form = CustomUserFrom()
    if request.method == 'POST':
        form = CustomUserFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'registration succesfull')
            return redirect('/loginpage')
    return render(request, 'blog/pages/register.html', {'form': form})


def loginpage(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, 'logged in succesfully')
            return redirect('/')
        else:
            messages.error(request, 'invalid username or password')
            return redirect('/loginpage')
    return render(request, 'blog/pages/login.html')


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'logged out succesfully')
    return redirect('/')


def detailedview(request, cname, aname):
    if (Category.objects.filter(name=cname, status=0)):
        if (Article.objects.filter(title=aname)):
            article = Article.objects.filter(title=aname).first()
            return render(request, 'blog/pages/detailedview.html', {'article': article})
        else:
            messages.error(request, 'no such artice found')
            return redirect('topicarticlepage')
    else:
        messages.error(request, 'no such artice found')
        return redirect('topicarticlepage')


def fav(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            article_id = data['aid']
            product_status = Article.objects.get(id=article_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id, article_id=article_id):
                    return JsonResponse({'status': 'article already in saved posts'})
                else:
                    Favourite.objects.create(
                        user=request.user, article_id=article_id)
                    return JsonResponse({'status': 'article added to saved posts'})

        else:
            return JsonResponse({'status': 'login to add favourite'}, status=200)

    else:
        return JsonResponse({'status': 'invalid access'}, status=200)


def savedpage(request):
    if request.user.is_authenticated:
        saved = Favourite.objects.filter(user=request.user)
        print(saved)
        return render(request, 'blog/pages/saved.html', {'saved': saved})
    else:
        return redirect('/')


def remove_favourite(request, fid):
    item = Favourite.objects.get(id=fid)
    item.delete()
    return redirect('/savedpage')
