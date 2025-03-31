from django.urls import path
from .views import EventFilterView, EventListCreateView, EventDetailView, EventSearchView

urlpatterns = [
    path("event/", EventListCreateView.as_view(), name="event-list-create"),
    path("event/<int:pk>/", EventDetailView.as_view(), name="event-detail"),
    path("event/filter/", EventFilterView.as_view(), name="event-filter"),
    path("event/search/", EventSearchView.as_view(), name="event-search"),
]