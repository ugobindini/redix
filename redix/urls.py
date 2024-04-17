from django.urls import path
from os.path import isfile

from . import views

from file_manager import *

urlpatterns = [path('home', views.index, name='index'), path('', views.figured_bass, name='fb'),
	path('get_humdrum_snippet/<str:item_id>', views.get_humdrum_snippet, name='get_humdrum_snippet'),
	path('get_item_list/<str:stat_id>', views.get_item_list, name='get_item_list'), ]


# DEVELOPER NOTE: it is highly unelegant to put this code here,
# but in apps.py it was not working

def load_new_pieces():
	# TODO: write a function to include new user-defined pieces
	return


print(f"The database contains {len(Piece.objects.all())} pieces.")

load_composers(verbose=False)
