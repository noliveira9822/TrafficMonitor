from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from .views import *

urlpatterns = [
    path('getsegments', get_traffic_segments),
    path('addsegment', add_segment),
    path('updatesegment/<int:segment_id>', update_segment),
    path('deletesegment/<int:segment_id>', delete_segment),
    path('docs/', include_docs_urls(title='Traffic Segment API')),
]