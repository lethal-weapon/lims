from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from bulletin.models import Article


@login_required(login_url=reverse_lazy('login'))
def site_news(request):
    return render(request, 'bulletin/news.html', {
        'article_list': Article.objects.order_by('-published')[7:]
    })
