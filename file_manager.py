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

def string_to_html_string(s):
	# given a string (composer name), it returns a string consisting only of the letters. * is replaced by x
	res = ''.join(filter(str.isalpha, s))
	if s.endswith('*'):
		return res + 'x'
	else:
		return res


def load_cint_lines(path):
	# given a path of the form Jos/filename.krn", returns the list of lists of strings in cint format
	cint_filename = CINT_DIR + "/" + path.split("/")[-1][:-4] + ".txt"
	if not os.path.isfile(cint_filename):
		# create the file with a bash command
		out_file = open(cint_filename, "w")
		shell_command = f"cint {KRN_DIR}/{path} --pitch -r"
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
	omd = ""
	otl = ""
	atr = ""
	test_print = True
	for line in lines:
		if not len(coa) and line.startswith("!!!COA"):
			coa = line.split(':')[1][1:-1]
			coa_check = True
		if not len(com) and line.startswith("!!!COM"):
			com = line.split(':')[1][1:-1]
			com_check = True
		if not len(opr) and line.startswith("!!!OPR"):
			opr = line.split(':')[1][1:-1]
		if not len(omd) and line.startswith("!!!OMD"):
			omd = line.split(':')[1][1:-1]
		if not len(otl) and line.startswith("!!!OTL"):
			otl = line.split(':')[1][1:-1]
		if not len(atr) and line.startswith("!!attribution-level@Jos"):
			atr = line.split(':')[1][1:-1]

	# Cleaning of composer names
	if len(coa):
		composer = coa + "*"
	else:
		composer = com

	# Set capital first letter
	composer = composer[0].upper() + composer[1:]

	# In JRP, dubious pieces are included in the Jos folder, with various attribution levels
	if path.startswith("Jos"):
		if atr.startswith("1") or atr.startswith("2"):
			composer = "Des Prez, Josquin"
		else:
			composer = "Des Prez, Josquin*"

	if len(opr):
		title = opr
		if len(omd):
			title += " / " + omd
		if len(otl):
			title += " / " + otl
	else:
		title = otl

	return Piece(path=path, composer=composer, title=title)


def points_from_path(path):
	# collect points from file to a list. Note: path is of the form Xxx/file
	lines = load_cint_lines(path)
	for line in lines:
		point = line_to_point(path, line)
		if point is not None:
			yield point


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


def load_composers(verbose=False):
	# starting from the pieces in the database, list the composers
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
		COMPOSERS.append(Composer(name=composer, html_name=string_to_html_string(composer), dates=dates, n_pieces=name_to_n[composer]))

	# create bakwards table to convert html names (used for id of html elements) to actual composer names
	for composer in COMPOSERS:
		HTML_NAME_TO_COMPOSER[composer.html_name] = composer.name

	# sort alphabetically
	COMPOSERS.sort(key=lambda x: x.name)
	if verbose:
		for composer in COMPOSERS:
			print(composer)


def out_tex_table(filename):
	out_file = open(filename, 'w')
	for composer in COMPOSERS:
		if composer.name.startswith("Palestrina"):
			piece_titles = [piece.title for piece in Piece.objects.filter(composer__exact=composer.name)]
			piece_titles.sort()
			for title in piece_titles:
				out_file.write(f"{title} & \\\\\n")
			out_file.write(f"\\hline\n")
	out_file.close()