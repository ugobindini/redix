# automatic basso continuo ciphering of music, based on humdrumm tools and krn files

import os
import argparse

# from constants import *
# from piece import Piece
# from stat_manager import StatManager, collect_points


# def show_points(key_type, points_list, show_all):
# 	points_by_key = {}
# 	for point in points_list:
# 		if key_type == 'c':
# 			key = point.reduced_chord
# 		elif key_type == 'f':
# 			key = point.full_chord
# 		elif key_type == 'r':
# 			key = point.resolution_string_key()
# 		else:
# 			key = None
# 		if key not in points_by_key.keys():
# 			points_by_key[key] = []
# 		points_by_key[key].append(point)
#
# 	ordered_keys = sorted(points_by_key.keys(), key=lambda x: len(points_by_key[x]), reverse=True)
#
# 	back = False
# 	while back == False:
# 		for n, key in enumerate(ordered_keys):
# 			num_points = len(points_by_key[key])
# 			extra_char = 's' if num_points > 1 else ''
# 			print(
# 				f'{n}\t{key} {num_points} point{extra_char} ({num_points * 100 / len(points_list):4f}%)')
# 			if show_all:
# 				for point in points_by_key[key]:
# 					print(point)
# 		print("Expand line number ('b' for back) ")
# 		next_query = input()
# 		if next_query == 'b':
# 			back = True
# 		else:
# 			print("Select key: c = ciphering, f = full chord, r = resolution ")
# 			next_key_type = input()
# 			print("Show details for all points? (y/n)")
# 			next_show_all = True if input() == 'y' else False
# 			show_points(next_key_type, points_by_key[ordered_keys[int(next_query)]], next_show_all)
#
#
# def apply_filter(contains, does_not_contain, no_reduce):
# 	# generates a list of lists of points with the matching characteristics
#
# 	# handle the text input
# 	contains_list = contains.split(" ")
# 	does_not_contain_list = does_not_contain.split(" ")
# 	no_reduce_list = no_reduce.split(" ")
#
# 	# create a stat manager
# 	stat_manager = StatManager(contains=contains_list, does_not_contain=does_not_contain_list, no_reduce=no_reduce_list,
# 	                           quarters=args.quarters, voices=voices)
#
# 	# load all pieces
# 	all_pieces = []
# 	for filename in krn_files:
# 		if filename.endswith(".krn"):
# 			all_pieces.append(Piece(filename))
#
# 	# collect all points compatible with parameters
# 	all_points = collect_points(all_pieces, stat_manager)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-q", "--quarters", nargs='+', help="which quarters should be taken in a semibrevis (mod 4)",
	                    type=int)
	parser.add_argument("-c", "--contains", nargs='+', help="collect points with a supersset of this signature", type=int)
	parser.add_argument("-nc", "--does_not_contain", nargs='+', help="collect points whose signature does not intersect this",
	                    type=int)
	parser.add_argument("-v", "--voices", help="count only points with given number(s) of voices; format 1-2,4,6-7")
	parser.add_argument("-nr", "--no_reduce", nargs='+', help="this intervals are not reduced to within an octave",
	                    type=int)
	parser.add_argument("-s", "--show", action="store_true", help="Show details for all collected points")
	parser.add_argument("-f", "--folder", nargs='+', help="in which composer folder(s) should one search")
	args = parser.parse_args()

	# get list of voices numbers from string argument
	# if args.voices is not None:
	# 	voices_ranges = (x.split("-") for x in args.voices.split(","))
	# 	voices = [i for r in voices_ranges for i in range(int(r[0]), int(r[-1]) + 1)]
	# else:
	# 	voices = None
	#
	# # collect filenames from folders
	# if args.folder is not None:
	# 	krn_dirs = [KRN_DIR + "/" + x for x in args.folder]
	# else:
	# 	krn_dirs = [KRN_DIR + "/" + directory for directory in os.listdir(KRN_DIR) if directory[0] != '.']
	#
	# krn_files = [directory + "/" + file for directory in krn_dirs for file in os.listdir(directory)]
	#
	# stat_manager = StatManager(contains=args.contains, does_not_contain=args.does_not_contain, no_reduce=args.no_reduce,
	#                                    quarters=args.quarters, voices=voices)

	# load all pieces
	# all_pieces = []
	# for filename in krn_files:
	# 	if filename.endswith(".krn"):
	# 		all_pieces.append(Piece(filename))
	#
	# print(f"Loaded {len(all_pieces)} pieces from {len(krn_dirs)} directories.")
	#
	# composers = list(set([piece.attributed_composer() for piece in all_pieces if piece.attributed_composer() is not None]))
	# composers.sort()

	filenames = [x for x in os.listdir(args.folder[0]) if not x.startswith('.')]
	search_text = "Perluigi"
	replace_text = "Pierluigi"

	for filename in filenames:
		path = f"{args.folder[0]}/{filename}"
		with open(path, 'r') as file:
			data = file.read()
			data = data.replace(search_text, replace_text)

		with open(path, 'w') as file:
			file.write(data)


	# collect all points compatible with parameters
	# all_points = collect_points(all_pieces, stat_manager)
	#
	# print("Collected ", len(all_points), " points")
	#
	# show_points(key_type='c', points_list=all_points, show_all=args.show)
