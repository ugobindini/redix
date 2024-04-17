# this class represent a piece, consisting of a list of points and some metadata info

from file_manager import load_cint_lines, line_to_point


class Piece:
	def __init__(self, filename):
		self.filename = filename

		# load metadata
		self.metadata = {}
		lines = open(self.filename, "r").readlines()
		i = 0
		while lines[i][:3] == "!!!":
			if lines[i][3:6] not in self.metadata.keys():
				self.metadata[lines[i][3:6]] = lines[i][8:-1]
			i += 1

		# load points
		self.points = []
		cint_lines = load_cint_lines(filename)
		for k in range(len(cint_lines)):
			point = line_to_point(self, cint_lines[k])
			if point is not None:
				self.points.append(point)

	def composer(self):
		if "COM" in self.metadata.keys():
			return self.metadata["COM"]
		else:
			return None

	def attributed_composer(self):
		if "COA" in self.metadata.keys():
			return self.metadata["COA"]
		else:
			return self.composer()

		"""
			if point is not None:
				if self.voices is None or point.voices in self.voices:
					if point.is_dissonant():
						# add resolution chain
						point.resolution = []
						if k < len(cint_lines) - 1:
							h = 1
							next_point = self.line_to_point(cint_lines[k + h], metadata=None)
							while next_point.is_dissonant():
								point.resolution.append(next_point)
								h += 1
								if k + h >= len(cint_lines):
									print("WARNING: piece ends on a dissonance!")
									print(metadata)
									break
								else:
									next_point = self.line_to_point(cint_lines[k + h], metadata=None)
							point.resolution.append(next_point)
					self.points_list.append(point)

		# final check to match the queries explore and explorex
		if self.explore is not None:
			res = [x for x in res if x.reduced_chord == tuple(self.explore)]
		if self.explorex is not None:
			res = [x for x in res if set(self.explorex).issubset(set(x.reduced_chord))]
		return res
		"""