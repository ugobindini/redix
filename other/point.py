# this class represents a ciphering point
# it brings ciphering information (base note, chord) and meta information (name of the piece, bar)

from constants import *

def sign(x):
	if x >= 0:
		return 1
	else:
		return -1


def pair_to_interval(a, b):
	# returns the difference of the two numbers + 1
	return sign(b - a) * (abs(b - a) + 1)


class Point:
	def __init__(self, piece, absq, bar, beat, notes):
		self.piece = piece
		self.absq = absq
		self.bar = bar
		self.beat = beat
		self.notes = notes # this does not contain zeroes
		self.base_note = min(self.notes)
		self.full_chord = tuple([note - self.base_note + 1 for note in self.notes])
		self.voices = len(self.notes)
		self.reduced_chord = None
		self.resolution = None

	def __repr__(self):
		res = f'{PITCH_7[self.base_note % 7]}{self.full_chord}, {self.voices} voices,  bar {self.bar}\n'
		if self.resolution is not None:
			res += f'Resolution: {PITCH_7[self.base_note % 7]}{self.full_chord}'
			base_note = self.base_note
			for point in self.resolution:
				res += f' -> {pair_to_interval(base_note, point.base_note)}{point.full_chord} t {point.quarter}'
				base_note = point.base_note
			res += "\n"
		for key in self.metadata.keys():
			if len(key) == 3:
				res += f'{key}: {self.piece.metadata[key]}\n'
		return res

	def resolution_string_key(self):
		# returns a (dict) key of string format to characterize resolutions
		res = f'{self.full_chord}'
		if self.resolution is not None:
			base_note = self.base_note
			for point in self.resolution:
				res += f' -> {pair_to_interval(base_note, point.base_note)}{point.full_chord}'
				base_note = point.base_note
		return res

	def is_dissonant(self):
		#true if the chord contains a dissonance, false otherwise
		if set(self.reduced_chord).issubset({3, 5}) or set(self.reduced_chord).issubset({3, 6}):
			return False
		else:
			return True
