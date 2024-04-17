import os
import matplotlib.pyplot as plt


def sign(x: int):
	if x != 0:
		return x // abs(x)
	else:
		return 0


def string_to_number(s):
	# choose the right type, int or float
	try:
		return int(s)
	except:
		return float(s)


color = {1: (0.0, 0.0, 1.0), -1: (0.6, 0.6, 1.0)}
size = {1: 100, -1: 50}

if __name__ == "__main__":
	cint_files = os.listdir("cint_files")
	files = []
	for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
		files += [x for x in cint_files if x.startswith(f"Rue1024{letter}-")]

	print(files)

	x = []
	y = []
	c = []
	s = []
	absq_offset = 0

	for file in files:
		lines = [line[:-1].split("\t") for line in open(f"cint_files/{file}", "r").readlines()[1:-1]]
		for line in lines:
			for note in line[3:]:
				int_note = int(note)
				if int_note:
					x.append(string_to_number(line[0]) + absq_offset)
					y.append(abs(int_note))
					c.append(color[sign(int_note)])
					s.append(size[sign(int_note)])

		absq_offset += string_to_number(lines[-1][0]) + 8

	plt.scatter(x, y, s=s, c=c, linewidth=0)
	plt.show()





