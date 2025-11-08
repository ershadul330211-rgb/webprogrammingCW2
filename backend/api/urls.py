from django.urls import path
from . import views

urlpatterns = [
    # /api/characters/ -> GET (list), POST (create)
    path('characters/', views.character_list_create, name='character-list-create'),
    
    # /api/characters/1/ -> PUT (update), DELETE (destroy)
    path('characters/<int:pk>/', views.character_detail_update_delete, name='character-detail'),
    
    # /api/quotes/ -> POST (create)
    path('quotes/', views.quote_create, name='quote-create'),
    
    # /api/quotes/1/ -> PUT (update), DELETE (destroy)
    path('quotes/<int:pk>/', views.quote_detail_update_delete, name='quote-detail'),
]