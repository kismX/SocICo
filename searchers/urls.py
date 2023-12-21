from django.urls import path
from .views import user_filter, add_terms, terms_list_view, remove_terms

urlpatterns = [
    path('user_filter/', user_filter, name='user_filter'),
    path('add_terms/', add_terms, name='add_terms'),
    path('terms_list/', terms_list_view, name='terms_list'),
    path('delete_term/<int:term_id>/', remove_terms, name='delete_term'),
]