import os
f = "/Users/Changye/Downloads/maildir/"
docs = []
for r, d, f in os.walk(f):
	s = r.split("/")[-1]
	for files in f :
		if "DS_Store" not in files and "sent" in s:
			st = r + "/" + files
			docs.append(st)
with open("file_path.txt", "w") as fout:
	for each in docs:
		fout.write(each + "\n")