from django.urls import path, re_path
# from django.conf.urls import patterns

from . import views
from django.conf import settings

app_name='polls'
urlpatterns = [
    path('', views.track, name='track'),
    # path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('detail/', views.track, name='track'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

# urlpatterns += re_path('django.views.static',(r'^media/(?P<path>.*)','serve',{'document_root':settings.MEDIA_ROOT}))
# print(urlpatterns)
