from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Article, FacilitySchedule


# display future schedules and top 7 latest articles
@login_required(login_url=reverse_lazy('login'))
def site_bulletin(request):
    return render(request, 'bulletin/bulletin.html', {
        'article_list' : Article.objects.order_by('-published')[:7],
        'schedule_list': FacilitySchedule.objects.filter(
            day__gte=datetime.today().date())
    })


# display the rest of articles
@login_required(login_url=reverse_lazy('login'))
def site_news(request):
    return render(request, 'bulletin/news.html', {
        'article_list': Article.objects.order_by('-published')[7:]
    })
