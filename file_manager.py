import os
import subprocess
import re

from constants import *
from redix.models import Piece, Point, list_to_string
from composers import *

def string_to_number(s):
	# choose the right type, int or float
	try:
		return int(s)
	except:
		return float(s)


def load_cint_lines(filename):
	# given a filename which ends with ".krn", returns the list of lists of strings in cint format
	cint_filename = CINT_DIR + "/" + filename.split("/")[-1][:-4] + ".txt"
	if not os.path.isfile(cint_filename):
		# create the file with a bash command
		out_file = open(cint_filename, "w")
		shell_command = "cint " + filename + " --pitch -r"
		output = subprocess.check_output(shell_command, shell=True, universal_newlines=True)
		out_file.write(output)

	assert os.path.isfile(cint_filename)
	# remove final \n character and split as list
	cint_lines = [x[:-1].split("\t") for x in open(cint_filename, "r").readlines()[1:-1]]
	return [[string_to_number(s) for s in line] for line in cint_lines]


def line_to_point(path, line):
	absq, bar, beat = tuple(line[:3])
	notes = [abs(x) for x in line[3:] if x]
	if len(notes):
		notes.sort()
		base_note = min(notes)
		full_chord = [x - base_note + 1 for x in notes[1:]]
		reduced_chord = [((x - 1) % 7) + 1 for x in full_chord]
		return Point(absq=absq, absq_mod4=absq % 4, bar=bar, beat=beat,
		             base_note=base_note, full_chord=list_to_string(full_chord),
		             reduced_chord=list_to_string(reduced_chord), voices=len(notes))
	else:
		return None


def piece_from_path(path):
	# Get the data from the krn file path, and return an instance of Piece
	lines = open(f"{KRN_DIR}/{path}", "r").readlines()
	com = ""
	coa = ""
	opr = ""
	otl = ""
	for line in lines:
		if not len(coa) and line.startswith("!!!COA"):
			coa = line.split(':')[1][1:-1]
			coa_check = True
		if not len(com) and line.startswith("!!!COM"):
			com = line.split(':')[1][1:-1]
			com_check = True
		if not len(opr) and line.startswith("!!!OPR"):
			opr = line.split(':')[1][1:-1]
		if not len(otl) and line.startswith("!!!OTL"):
			otl = line.split(':')[1][1:-1]

	# Cleaning of composer names
	if len(coa):
		composer = coa + "*"
	else:
		composer = com

	# Set capital first letter
	composer = composer[0].upper() + composer[1:]

	if path.startswith("Jos") and not composer.startswith("Des Prez"):
		composer = "Des Prez, Josquin*"

	if len(opr):
		title = opr
		if len(otl):
			title += " / " + otl
	else:
		title = otl

	return Piece(path=path, composer=composer, title=title)


def points_from_path(path):
	# collect points from file to a list
	res = []
	lines = load_cint_lines(path)
	for line in lines:
		point = line_to_point(path, line)
		if point is not None:
			res.append(point)
	return res


def load_pieces():
	n = 0
	for directory in os.listdir(KRN_DIR):
		if not directory.startswith('.'):
			for filename in os.listdir(f"{KRN_DIR}/{directory}"):
				if not filename.startswith('.'):
					path = f"{directory}/{filename}"
					piece = piece_from_path(path)
					piece.save()
					n += 1
	print(f"Loaded {n} pieces.")


def load_points():
	n = 0
	for piece in Piece.objects.all():
		path = piece.path
		for point in points_from_path(path):
			point.piece = piece
			point.save()
			n += 1
	print(f"Loaded {n} points.")


def load_composers():
	name_to_n = {}
	for piece in Piece.objects.all():
		composer = piece.composer
		if composer not in name_to_n.keys():
			name_to_n[composer] = 1
		else:
			name_to_n[composer] += 1
	for composer in name_to_n.keys():
		if composer in COMPOSER_DATES.keys():
			dates = COMPOSER_DATES[composer]
		else:
			dates = ""
		COMPOSERS.append(Composer(name=composer, dates=dates, n_pieces=name_to_n[composer]))

	COMPOSERS.sort(key=lambda x: x.name)