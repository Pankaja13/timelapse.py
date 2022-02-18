import subprocess
import os
import datetime
import sys

framerate = 60
skips = 5

directory = 'source/'
extensions = (['.jpg', '.jpeg'])

try:
	file_list = os.listdir(directory)
except FileNotFoundError:
	print("source folder not found")
	sys.exit(-1)

print(len(file_list), 'files in source dir')
print('At', framerate, 'fps, output will be', round(len(file_list)/(framerate*skips)), 'seconds long')
if input("Continue? (y/n)") != 'y':
	sys.exit(0)

files = []

for file in file_list:
	filename, extension = os.path.splitext(file)
	if extension.lower() in extensions:
		file_path = directory + file
		create_time = os.path.getctime(file_path)
		time_obj = datetime.datetime.fromtimestamp(create_time)
		file = {
			'file_path': file_path,
			'created_time': time_obj,
		}
		files.append(file)

files.sort(key=lambda x: x['created_time'])

try:
	input_file = open("input.txt", "w")
	for number, file in enumerate(files):
		if number % skips == 0:
			input_file.write('file ' + file['file_path'] + '\n')
	input_file.close()

	subprocess.run(['ffmpeg.exe', '-r', str(framerate), '-f', 'concat', '-i', 'input.txt', '-c:v', 'libx264', '-y',
		'-pix_fmt', 'yuv420p', 'output.mp4'])
finally:
	os.remove("input.txt")
