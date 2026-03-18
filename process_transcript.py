import re
import os
from datetime import datetime

def list_files_recursive(path='.'):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_recursive(full_path)
        else:
            print(full_path)

data_folder = '../data'
video_folders = []

for video_folder in os.listdir(data_folder):
     full_path = os.path.join(data_folder, video_folder)
     video_folders.append(full_path)

# print(video_folders)
#video_folders = ["..\\data\\2026-2-25-spirituality-for-atheists-sam-harris_2"]

class VideoData:
    def __init__(self):
        self.folder_name = ""
        self.url = ""
        self.date = datetime(1970, 11, 18)
        self.type = ""
        self.topic = ""
        self.direct_audience = ""
        self.other_audience = ""
        self.d = dict()
        self.data_dennett = dict()
        self.data_harris = dict()

videos = dict()
religious_groups = []
total_found_words = 0
dennett_by_years = dict()
harris_by_years = dict()

for folder_name in video_folders:
    transcript = os.path.join(folder_name, "transcript.txt")
    file = open(transcript)

    video_data = VideoData()
    video_data.folder_name = folder_name

    video_data.url = file.readline()
    for video_folder in videos:
        if video_data.url == videos[video_folder].url:
            print("video already processed ", folder_name)

    date_line = file.readline().split()
    if len(date_line) < 4:
        print("Error in file:", folder_name)
    if date_line[0] != "Date:":
        print("Error date_line in file:", folder_name)
    video_data.date = datetime(int(date_line[3]), int(date_line[2][:-1]), int(date_line[1][:-1]))

    type_line = file.readline().split()
    if len(type_line) < 4:
        print("Error in file:", folder_name)
    if type_line[0] != "Type" and type_line[1] != "of" and type_line[2] != "video:":
        print("Error type_line in file:", folder_name)
    video_data.type = type_line[3]

    topic_line = file.readline().split()
    if len(topic_line) == 0:
        print("Error in file:", folder_name)
    if topic_line[0] != "Topic:":
        print("Error topic_line in file:", folder_name)
    video_data.topic = topic_line[1]

    direct_audience_line = file.readline().split()
    if len(direct_audience_line) < 3:
        print("Error in file:", folder_name)
    if direct_audience_line[0] != "Direct" and direct_audience_line[1] != "audience:":
        print("Error direct_audience_line in file:", folder_name)
    video_data.direct_audience = direct_audience_line[2]

    other_audience_line = file.readline().split()
    if len(other_audience_line) < 3:
        print("Error in file:", folder_name)
    if other_audience_line[0] != "Other" and other_audience_line[1] != "audience:":
        print("Error other_audience_line in file:", folder_name)
    video_data.other_audience = other_audience_line[2]

    current_data_type = ""

    line_number = 0

    current_speaker = ""
    while True:
        line = file.readline()
        if not line:
            break
        line_tokens = line.split(' ', 1)
        if len(line_tokens) > 0:
            if line[0] == '#':
                if len(line_tokens) > 1:
                    current_data_type = line_tokens[1]
                    if current_data_type not in religious_groups:
                        religious_groups.append(current_data_type)
                else:
                    current_data_type = ""
                line_number = line_number + 1
                continue

            if current_data_type != "":
                if current_speaker == "Sam Harris":
                    if current_data_type not in video_data.data_harris:
                        video_data.data_harris[current_data_type] = ""
                    video_data.data_harris[current_data_type] = video_data.data_harris[current_data_type] + line
                elif current_speaker == "Daniel Dennett":
                    if current_data_type not in video_data.data_dennett:
                        video_data.data_dennett[current_data_type] = ""
                    video_data.data_dennett[current_data_type] = video_data.data_dennett[current_data_type] + line
                else:
                    print("Error, getting data before speaker name", line)

            if line[0] == '[':
                if line.startswith("[Sam Harris]:"):
                    current_speaker = "Sam Harris"
                elif line.startswith('[Daniel Dennett]:'):
                    current_speaker = "Daniel Dennett"
                elif not line.startswith('[Speaker'):
                    print("Error wrong speaker:", line)

        line_number = line_number + 1

    for data_type in video_data.data_dennett:
        print("Data Dennett", data_type, video_data.folder_name)
        word_count = len(video_data.data_dennett[data_type].split())
        total_found_words = total_found_words + word_count
        print(word_count)
        if not video_data.date.year in dennett_by_years:
            dennett_by_years[video_data.date.year] = 0
        dennett_by_years[video_data.date.year] = dennett_by_years[video_data.date.year] + word_count

    for data_type in video_data.data_harris:
        print("Data Harris",data_type, video_data.folder_name)
        word_count = len(video_data.data_harris[data_type].split())
        total_found_words = total_found_words + word_count
        print(word_count)
        if not video_data.date.year in harris_by_years:
            harris_by_years[video_data.date.year] = 0
        harris_by_years[video_data.date.year] = harris_by_years[video_data.date.year] + word_count

    videos[folder_name] = video_data

    file.close()


counts_by_types_dennett = dict()
counts_by_types_harris = dict()
for video_data in videos:
    print(videos[video_data].url)
    for about_people in videos[video_data].data_dennett:
        if about_people not in counts_by_types_dennett:
            counts_by_types_dennett[about_people] = 0
        counts_by_types_dennett[about_people] = counts_by_types_dennett[about_people] + len(videos[video_data].data_dennett[about_people].split())

    for about_people in videos[video_data].data_harris:
        if about_people not in counts_by_types_harris:
            counts_by_types_harris[about_people] = 0
        counts_by_types_harris[about_people] = counts_by_types_harris[about_people] + len(videos[video_data].data_harris[about_people].split())

print("Dennett:")
for about_people in counts_by_types_dennett:
    print(about_people, counts_by_types_dennett[about_people])

print("Harris:")
for about_people in counts_by_types_harris:
    print(about_people, counts_by_types_harris[about_people])


for group in religious_groups:
    print(group)


print("Dennett:")
dennett_total = 0
for year in dennett_by_years:
    print(year, dennett_by_years[year])
    dennett_total = dennett_total + dennett_by_years[year]
print("dennett_total: ", dennett_total)

print("Harris:")
harris_total = 0
for year in harris_by_years:
    print(year, harris_by_years[year])
    harris_total = harris_total + harris_by_years[year]
print("harris_total: ", harris_total)



# for file_name in file_names:
#     file = open(file_name)
#     speaker = ""
#     lineNumber = 0
#     while True:
#         line = file.readline()
#         lineNumber = lineNumber + 1
#         if line.startswith('#'):
#             if line.startswith('# DD') or line.startswith('# SH') or line.startswith('# Dawkins') or line.startswith('# Hitchens'):
#                 print(line)
#                 speaker = line[2:4]
#             elif line != '#':
#                 print("error on line number ", lineNumber, ", line: ", line)
#             speaker = line[2:4]        
#             continue
#         elif re.match(r"\d\d:\d\d:\d\d", line) is not None:
#             print(line)
#         elif speaker == 'DD' or speaker == 'SH':
#             print(line)


#         if len(line) > 0 and line[0].isdigit() and re.match(r"\d\d:\d\d:\d\d", line) is None:
#             print("error on line number ", lineNumber, ", line: ", line)
#         if len(line) > 0 and not line[0].isdigit() and not line[0].isalpha() :
#             print("error on line number ", lineNumber, ", line: ", line)

#         if len(line) == 0:
#             break

#     file.close()
