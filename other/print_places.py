import os
import subprocess
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--command", help="cint command to be executed, with parameter --search")
	args = parser.parse_args()

	lines = subprocess.check_output(args.command, shell=True, universal_newlines=True).split("\n")

	printed = False
	for line in lines:
		if line.startswith("!!!COM") or line.startswith("!!!COA"):
			composer = line.split(':')[-1][1:]
			printed = False
		if line.startswith("!!!OTL"):
			title = line.split(':')[-1][1:]
			printed = False
		if line.startswith("="):
			measure = ""
			i = 1
			while line[i].isnumeric():
				measure += line[i]
				i += 1
			printed = False
		if not line.startswith("!") and not line.startswith("*"):
			if line.__contains__('@') and not printed:
				print(f"{composer} - {title}, bar {measure}.")
				printed = True