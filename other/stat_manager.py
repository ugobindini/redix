# this class contains the requested keys for statistics collection

class StatManager:
	def __init__(self, contains: list[int], does_not_contain: list[int], no_reduce: list[int], quarters: list[int], voices: list[int]):
		self.contains = set(contains) if contains is not None else None
		self.does_not_contain = set(does_not_contain) if does_not_contain is not None else None
		self.no_reduce = no_reduce
		self.quarters = quarters
		self.voices = voices

	def reduce_interval(self, x):
		# reduction mod 7, but keeping the intervals in no_reduce and reducing their over-octaves to them
		if self.no_reduce is not None:
			check_list = [(x - y) % 7 for y in self.no_reduce if x >= y]
			if 0 in check_list:
				return min([y for y in self.no_reduce if y % 7 == x % 7])
			else:
				return (x - 1) % 7 + 1
		else:
			return (x - 1) % 7 + 1

	def set_reduced_chord(self, point):
		point.reduced_chord = set([self.reduce_interval(x) for x in point.full_chord])
		point.reduced_chord.remove(1)  # do not write unison in ciphering
		point.reduced_chord = tuple(sorted(set(point.reduced_chord)))


def collect_points(pieces, stat_manager):
	# given a list of pieces and the stat_manager, collect the compatible points
	res = []
	j = 0
	for piece in pieces:
		for point in piece.points:
			if stat_manager.voices is None or point.voices in stat_manager.voices:
				if stat_manager.quarters is None or point.absq % 4 in stat_manager.quarters:
					stat_manager.set_reduced_chord(point)
					if stat_manager.does_not_contain is None or point.reduced_chord & stat_manager.does_not_contain == emptyset:
						if stat_manager.contains is None or stat_manager.contains.issubset(set(point.reduced_chord)):
							res.append(point)
	return res