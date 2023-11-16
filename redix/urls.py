from django.urls import path

from . import views

from file_manager import *


urlpatterns = [
    path('', views.index, name='index'),
    path('fb', views.figured_bass, name='fb'),
    path('get_humdrum_snippet/<str:item_id>', views.get_humdrum_snippet, name='get_humdrum_snippet'),
    path('get_item_list/<str:stat_id>', views.get_item_list, name='get_item_list'),
]

def delete_points():
    for point in Point.objects.filter(piece__path__contains="Xxx"):
        point.delete()


def delete_pieces():
    for piece in Piece.objects.filter(path__contains="Xxx"):
        piece.delete()


# delete_points()
# delete_pieces()
# load_pieces()
# load_points()

load_composers()
# for composer in COMPOSERS:
#     print(repr(composer.name))
