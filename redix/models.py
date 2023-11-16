from django.db import models
from dataclasses import dataclass
import subprocess

from constants import KRN_DIR
from composers import COMPOSER_DATES


def list_to_string(l, square=False):
	# a strange (but useful) format: ",1,2,3,"
	res = ','.join(str(x) for x in l)
	if square:
		return f"[{res}]"
	else:
		return f",{res},"


def string_to_list(s):
	if len(s) > 2:
		return [int(ch) for ch in s[1:-1].split(',')]
	else:
		return []


class Piece(models.Model):
	path = models.CharField(max_length=128)
	composer = models.CharField(max_length=128) # if it is not sure, it is terminated by *
	title = models.CharField(max_length=128)
	# attributed_composer = models.CharField(max_length=128)
	# composer_dates = models.CharField(max_length=64)
	# title = models.CharField(max_length=128)
	# genre = models.CharField(max_length=128)
	# piece_voices = models.IntegerField()

	def point_list(self):
		return Point.objects.filter(piece__path__exact=self.path)


class Point(models.Model):
	piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
	absq = models.FloatField()
	absq_mod4 = models.FloatField()
	bar = models.IntegerField()
	beat = models.IntegerField()
	base_note = models.IntegerField()
	# base_note_name = models.CharField(max_length=8)
	reduced_chord = models.CharField(max_length=128)
	full_chord = models.CharField(max_length=128)
	voices = models.IntegerField()
	# len_segment = models.IntegerField() # distance to the next root chord

	def __str__(self):
		return f"{self.piece.composer} - {self.piece.title}, bar {self.bar}, beat {self.beat}"

	def key(self, no_reduce):
		# takes as argument a list of integers: these intervals should not be reduced within an octave
		output = []
		for x in string_to_list(self.full_chord):
			if x in no_reduce:
				output.append(x)
			elif x % 7 != 1:
				output.append(((x - 1) % 7) + 1)
		output = list(set(output))
		output.sort()
		return list_to_string(output, square=True)

	def html_id(self):
		return f"point-{self.id}"

	def humdrum_snippet(self):
		# TODO: if bar is the last one, this might crash? Maybe save in Piece the number pf bars of the piece
		return subprocess.check_output(f"myank -m {max(self.bar-1, 0)}-{self.bar+1} {KRN_DIR}/{self.piece.path}", shell=True)

	def is_root_chord(self):
		if len(self.reduced_chord):
			x = set(string_to_list(self.reduced_chord))
			return x.issubset({1, 3, 5})
		else:
			return True

	def is_sixth_chord(self):
		# to improve performance, this assumes that the point is NOT root chord
		x = set(string_to_list(self.reduced_chord))
		return x.issuperset({6}) and x.issubset({1, 3, 6})

	def set_len_segment(self):
		res = 0
		start = self
		end = self
		try:
			next_point = Point.objects.get(pk=end.id+1)
		except:
			# we are at the end of the database
			self.len_segment = res
			self.save()
			return
		while next_point.piece.path == start.piece.path and not next_point.is_root_chord():
			end = next_point
			res += 1
			try:
				next_point = Point.objects.get(pk=end.id+1)
			except:
				# we are at the end of the database
				self.len_segment = res
				self.save()
				return
		if next_point.piece.path == start.piece.path:
			end = next_point
			res += 1
		self.len_segment = res
		self.save()

	def segment(self):
		end = Point.objects.get(pk=self.id+self.len_segment)
		return Segment(start=self, end=end)


@dataclass
class Segment:
	piece: Piece
	start: Point
	end: Point
	bar: int

	def __init__(self, start: Point, end: Point):
		print(start.piece.path, start, end)
		self.start = start
		self.end = end
		assert start.piece.id == end.piece.id, "Start and end of segment belong to different pieces!"
		self.piece = start.piece
		self.bar = start.bar

	def __len__(self):
		return len(self.point_list())

	def point_list(self):
		# Returns an iterator on the points
		for i in range(self.start.id, self.end.id + 1):
			yield Point.objects.get(pk=i)

	def key(self, no_reduce):
		res = ""
		base_note = self.start.base_note
		for point in self.point_list():
			if point.id != self.start.id:
				# if not at the beginning, print the melodic interval of the bass
				next_base_note = point.base_note
				res += f" {next_base_note - base_note + 1} "
				base_note = next_base_note
			res += point.key(no_reduce)
		return res

	# TODO: define a hum_key which returns a printable humdrum snippet

	def html_id(self):
		return '-'.join([point.html_id() for point in self.point_list()])

	def humdrum_snippet(self):
		# TODO: same as for Point
		return subprocess.check_output(f"myank -m {max(self.start.bar - 1, 0)}-{self.end.bar + 1} {KRN_DIR}/{self.piece.path}", shell=True)


class Stat:
	id: int
	key: str
	html_id: str
	n: int
	ratio: float
	list_of_items: list

	def __init__(self, id, key):
		self.id = id
		self.key = key
		self.html_id = f"stat-{self.id}"
		self.n = 0
		self.ratio = 0
		self.list_of_items = []

	def add_item(self, item):
		self.list_of_items.append(item)
		self.n += 1
