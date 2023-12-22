from django.urls import path
from .views import user_filter, add_terms, remove_terms

urlpatterns = [
    path('user_filter/', user_filter, name='user_filter'),
    path('add_terms/', add_terms, name='add_terms'),
    path('delete_term/<int:term_id>/', remove_terms, name='delete_term'),
]