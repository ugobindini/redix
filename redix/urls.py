from django.urls import path
from os.path import isfile

from . import views

from file_manager import *

urlpatterns = [
    path('', views.index, name='index'),
    path('fb', views.figured_bass, name='fb'),
    path('get_humdrum_snippet/<str:item_id>', views.get_humdrum_snippet, name='get_humdrum_snippet'),
    path('get_item_list/<str:stat_id>', views.get_item_list, name='get_item_list'),
]

# NOTE: it is highly unelegant to put this code here (for populating the database on first launch if it is empty),
# but in apps.py it was not working

def load_database():
	print("The database was empty: populating ...", end=" ")
	load_pieces()
	load_points()
	print("done.")
	print(f"Database populated with {len(Piece.objects.all())} pieces, {len(Piece.objects.all())} points")


# if not Point.objects.all():
# 	# The database is empty
# 	load_database()
load_composers()