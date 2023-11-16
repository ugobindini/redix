from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q
from django.db.models.functions import Mod

from .models import Piece, Point, Stat
from composers import COMPOSERS


def index(request):
    pieces = Piece.objects.all()
    composers = list(set(Piece.objects.all().values_list('composer', flat=True)))
    composers.sort()

    return render(request, 'index.html', {'composers': composers, 'pieces': pieces})


stats = []
id_to_item = {}
id_to_stat = {}
key_to_stat = {}


def figured_bass(request):
    # get all pieces from database
    all_pieces = Piece.objects.all()
    all_composers = list(set(all_pieces.values_list('composer', flat=True)))
    all_composers.sort()

    # Reset the variables
    global stats, id_to_item, id_to_stat, key_to_stat
    stat_id = 0
    selected_items = 0
    total_items = 0
    item_ratio = 0
    stats = []
    id_to_item = {}
    id_to_stat = {}
    key_to_stat = {}

    if request.GET.get('search_points_btn') or request.GET.get('search_segments_btn'):
        # Collect request data from form
        filter_composers = [key for key in list(request.GET.keys()) if key in all_composers]
        print(filter_composers)
        piece_name = request.GET.get('fb_piece_name')
        contains = request.GET.get('fb_contains').split()
        does_not_contain = request.GET.get('fb_does_not_contain').split()
        no_reduce = [int(x) for x in request.GET.get('fb_no_reduce').split()]
        quarters = [i for i in range(4) if request.GET.get(f"quarter{i}") is not None]
        lowest_note = [int(x) for x in request.GET.get('lowest_note').split()]

        # Apply filters for composers and beats
        query = Q()
        for composer in filter_composers:
            query = query | Q(piece__composer__exact=composer)
        points = Point.objects.filter(query)

        if piece_name is not None:
            points = points.filter(piece__title__contains=piece_name)

        if len(quarters):
            query = Q()
            for x in quarters:
                query = query | Q(absq_mod4__exact=x)
            points = points.filter(query)

        if len(lowest_note):
            query = Q()
            for x in lowest_note:
                query = query | Q(base_note__exact=x)
            points = points.filter(query)

        # The total points in this absq position from this composer
        total_items = points.count()
        print(f"Total points {total_items}")

        for x in contains:
            points = points.filter(Q(reduced_chord__contains=f",{x},") | Q(full_chord__contains=f",{x},"))
        for x in does_not_contain:
            points = points.exclude(full_chord__contains=f",{x},")
            if x not in [y % 7 for y in no_reduce]:
                # none of the intervals which are asked not to be reduced matches the "does not contain"
                points = points.exclude(reduced_chord__contains=f",{x},")

        chord_type_count = {"root": 0, "sixth": 0, "dissonant": 0}

        # Compute statistics
        for point in points:
            item = point
            if point.is_root_chord():
                chord_type_count["root"] += 1
            elif point.is_sixth_chord():
                chord_type_count["sixth"] += 1
            else:
                chord_type_count["dissonant"] += 1
            id_to_item[item.html_id()] = item
            key = item.key(no_reduce)
            if key not in key_to_stat.keys():
                stat = Stat(id=stat_id, key=key)
                stat_id += 1
                stat.add_item(item)
                stats.append(stat)
                id_to_stat[stat.html_id] = stat
                key_to_stat[key] = stat
            else:
                key_to_stat[key].add_item(item)

        stats.sort(reverse=True, key=lambda x: x.n)
        selected_items = sum(chord_type_count.values())
        for stat in stats:
            if selected_items:
                stat.ratio = round(stat.n * 100 / selected_items, 2)
            else:
                stat.ratio = 0
        if total_items:
            item_ratio = round(selected_items * 100 / total_items, 2)
        else:
            item_ratio = 0

        # Nicely formatted list of selected composers
        f_selected_composers = ""
        for composer in filter_composers:
            f_selected_composers += f"{composer}; "
        f_selected_composers = f_selected_composers[:-2] + "."

        if len(quarters):
            beats = quarters
        else:
            beats = [x for x in range(4)]

        return render(request, 'figured_bass.html',
                  {'stats': stats,
                   'selected_items': selected_items,
                   'total_items': total_items,
                   'item_ratio': item_ratio,
                   'f_selected_composers': f_selected_composers,
                   'n_root': chord_type_count["root"],
                   'n_root_ratio': round(chord_type_count["root"] * 100 / selected_items, 2) if selected_items else 0,
                   'n_sixth': chord_type_count["sixth"],
                   'n_sixth_ratio': round(chord_type_count["sixth"] * 100 / selected_items, 2) if selected_items else 0,
                   'n_dissonant': chord_type_count["dissonant"],
                   'n_dissonant_ratio': round(chord_type_count["dissonant"] * 100 / selected_items, 2) if selected_items else 0,
                   'all_composers': COMPOSERS,
                   'beats': beats})

    else:
        return render(request, 'figured_bass.html',
                  {'all_composers': COMPOSERS})


def get_humdrum_snippet(request, item_id):
    global id_to_item
    item = id_to_item[item_id]
    return HttpResponse(item.humdrum_snippet())


def get_item_list(request, stat_id):
    global id_to_stat
    stat = id_to_stat[stat_id]
    res = "<table class='point-table'><tr><th class='point-data'></th><th class='point-data'>Composer</th><th class='point-data'>Title</th><th class='point-data'>Bar</th></tr>"
    for item in stat.list_of_items:
        res += f"<tr><td><button type = 'button' class ='key-btn light-btn' onclick=\"get_humdrum_snippet('get_humdrum_snippet/{item.html_id()}', '{item.html_id()}')\">Show</button></td>"
        res += f"<td class='point-data'>{item.piece.composer}</td><td class='point-data'>{item.piece.title}<td><td class='point-data'>{item.bar}</td></tr>"
        res += f"<tr><td></td><td colspan='3'><div class='humdrum-notation' id='{item.html_id()}' style='display: none;'></div></td></tr>"
    res += "</table>"

    return HttpResponse(res)

