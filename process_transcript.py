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

class DataSegmentInfo:
    def __init__(self, line):
        if line[0] != '#':
            print("Wrong segment label", line)
        
        if line[1] == 'N':   
            self.is_positive = False
        elif line[1] == 'P':   
            self.is_positive = True
        else:
            print("Wrong segment label positivity", line)

        self.specific_topic = ''
        if line[2] == 'A' or line[2] == 'D' or line[2] == 'S' or line[2] == 'T':   
            self.specific_topic = line[2]
        else:   
            print("Wrong segment label specific topic", line)

        if line[3] == 'J':   
            self.is_judging = True
        elif line[3] == ' ' and self.specific_topic == 'A':
            self.is_judging = True
        elif line[3] == ' ':
            self.is_judging = False
        else:
            print("Wrong segment label judging", line)

        line_tokens = line.split(' ', 1)
        self.group = line_tokens[1][:-1]


class VideoInfo:
    def __init__(self, line):
        self.year = 1970
        self.type = ""
        self.topic = ""
        self.direct_audience = ""
        self.other_audience = ""


class VideoData:
    def __init__(self):
        self.folder_name = ""
        self.url = ""
        self.date = datetime(1970, 11, 18)
        self.type = ""
        self.topic = ""
        self.direct_audience = ""
        self.other_audience = ""
        self.data_dennett = dict()
        self.data_harris = dict()


all_christians = ['About Christian fundamentalists', 'About Christians', 'About Christian theologians', 'About Christian preachers', 'About moderate Christians']
all_non_religious = ['About atheists', 'About secular people', 'About non-religious people', 'About scientists, secularists and atheists', 'About Christian preachers - atheists']
all_scientists = ['About scientists', 'About scientists, secularists and atheists']
all_muslims = ['About Muslims', 'About moderate Muslims', 'About Muslim fundamentalists']
all_religious_people_in_general = ['About religious people', 'About religious fundamentalists', 'About religious moderates']
other_religious_people = ['About other religious people']
christian_theologians = ['About Christian theologians']
all_religious_moderates = ['About moderate Christians', 'About moderate Muslims', 'About religious moderates']
all_religious_fundamentalists = ['About Christian fundamentalists', 'About Muslim fundamentalists', 'About religious fundamentalists']

def is_about(segment_info, groups, should_be_positive, is_directly):
    if segment_info.is_positive == should_be_positive:
        if segment_info.group in groups:
            if is_directly:
                if segment_info.specific_topic == 'A' or segment_info.is_judging:
                    return True
            else:
                if not segment_info.specific_topic == 'A' and not segment_info.is_judging:
                    return True
    return False


def save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, groups, folder_name, should_be_positive, is_directly):
    if not os.path.exists(str(".\data_for_emfd\\") + folder_name):
        os.makedirs(str(".\data_for_emfd\\") + folder_name)

    outputs_dennett = dict()
    for year in data_for_analysis_dennett:
        for about_people in data_for_analysis_dennett[year]:
            if is_about(about_people, groups, should_be_positive, is_directly):
                if not os.path.exists(str(".\data_for_emfd\\") + folder_name  + str("\\dennett")):
                    os.makedirs(str(".\data_for_emfd\\") + folder_name  + str("\\dennett"))
                with open(str(".\data_for_emfd\\") + folder_name + str("\\dennett\\") + str(year) + str(".txt"), "a") as file:
                    file.write(data_for_analysis_dennett[year][about_people])

    for year in data_for_analysis_harris:
        for about_people in data_for_analysis_harris[year]:
            if is_about(about_people, groups, should_be_positive, is_directly):
                if not os.path.exists(str(".\data_for_emfd\\") + folder_name  + str("\\harris")):
                    os.makedirs(str(".\data_for_emfd\\") + folder_name  + str("\\harris"))
                with open(str(".\data_for_emfd\\") + folder_name + str("\\harris\\") + str(year) + str(".txt"), "a") as file:
                    file.write(data_for_analysis_harris[year][about_people])


videos = dict()
religious_groups = []
video_types = []
topics = []
direct_audiences = []
indirect_audiences = []
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

    type_line = file.readline()
    if len(type_line) < 4:
        print("Error in file:", folder_name)
    if not type_line.startswith("Type of video:"):
        print("Error type_line in file:", folder_name)
    video_data.type = type_line[15:]
    if video_data.type not in video_types:
        video_types.append(video_data.type)

    topic_line = file.readline()
    if len(topic_line) == 0:
        print("Error in file:", folder_name)
    if not topic_line.startswith("Topic:"):
        print("Error topic_line in file:", folder_name)
    video_data.topic = topic_line[7:]
    if video_data.topic not in topics:
        topics.append(video_data.topic)

    direct_audience_line = file.readline()
    if len(direct_audience_line) < 3:
        print("Error in file:", folder_name)
    if not direct_audience_line.startswith("Direct audience:"):
        print("Error direct_audience_line in file:", folder_name)
    video_data.direct_audience = direct_audience_line[17:]
    if video_data.direct_audience not in direct_audiences:
        direct_audiences.append(video_data.direct_audience)

    other_audience_line = file.readline()
    if len(other_audience_line) < 3:
        print("Error in file:", folder_name)
    if not other_audience_line.startswith("Other audience:"):
        print("Error other_audience_line in file:", folder_name)
    video_data.other_audience = other_audience_line[16:]
    if video_data.other_audience not in indirect_audiences:
        indirect_audiences.append(video_data.other_audience)

    is_segment_relevant = False

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
                    current_data_type = DataSegmentInfo(line)
                    is_segment_relevant = True
                    #current_data_type = line_tokens[1][:-1]
                    if current_data_type.group not in religious_groups:
                        religious_groups.append(current_data_type.group)
                else:
                    is_segment_relevant = False
                line_number = line_number + 1
                continue

            if is_segment_relevant:
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

    # for data_type in video_data.data_dennett:
    #     print("Data Dennett", data_type, video_data.folder_name)
    #     word_count = len(video_data.data_dennett[data_type].split())
    #     total_found_words = total_found_words + word_count
    #     print(word_count)
    #     if not video_data.date.year in dennett_by_years:
    #         dennett_by_years[video_data.date.year] = 0
    #     dennett_by_years[video_data.date.year] = dennett_by_years[video_data.date.year] + word_count

    # for data_type in video_data.data_harris:
    #     print("Data Harris",data_type, video_data.folder_name)
    #     word_count = len(video_data.data_harris[data_type].split())
    #     total_found_words = total_found_words + word_count
    #     print(word_count)
    #     if not video_data.date.year in harris_by_years:
    #         harris_by_years[video_data.date.year] = 0
    #     harris_by_years[video_data.date.year] = harris_by_years[video_data.date.year] + word_count

    videos[folder_name] = video_data

    file.close()


counts_by_types_dennett = dict()
counts_by_types_harris = dict()
complete_data = dict()
data_for_analysis_dennett = dict()
data_for_analysis_harris = dict()
for folder_name in videos:
    print(videos[folder_name].url)
    year = videos[folder_name].date.year
    if len(videos[folder_name].data_dennett) > 0 and year not in data_for_analysis_dennett:
        data_for_analysis_dennett[year] = dict()

    for about_people in videos[folder_name].data_dennett:
        if about_people not in counts_by_types_dennett:
            counts_by_types_dennett[about_people] = 0
        counts_by_types_dennett[about_people] = counts_by_types_dennett[about_people] + len(videos[folder_name].data_dennett[about_people].split())

        if about_people not in complete_data:
            complete_data[about_people] = ""
        complete_data[about_people] = complete_data[about_people] + "\n " + folder_name + ", Dennett: \n"
        complete_data[about_people] = complete_data[about_people] + videos[folder_name].type + str(", ") + videos[folder_name].topic + str(", ")
        complete_data[about_people] = complete_data[about_people] + videos[folder_name].direct_audience + str(", ") + videos[folder_name].other_audience + "\n"
        complete_data[about_people] = complete_data[about_people] + videos[folder_name].data_dennett[about_people]

        if about_people not in data_for_analysis_dennett[year]:
            data_for_analysis_dennett[year][about_people] = ""
        data_for_analysis_dennett[year][about_people] = data_for_analysis_dennett[year][about_people] + videos[folder_name].data_dennett[about_people]

    if len(videos[folder_name].data_harris) > 0 and year not in data_for_analysis_harris:
        data_for_analysis_harris[year] = dict()

    for about_people in videos[folder_name].data_harris:
        if about_people not in counts_by_types_harris:
            counts_by_types_harris[about_people] = 0
        counts_by_types_harris[about_people] = counts_by_types_harris[about_people] + len(videos[folder_name].data_harris[about_people].split())
        
        if about_people not in complete_data:
            complete_data[about_people] = ""
        complete_data[about_people] = complete_data[about_people] + "\n " + folder_name + ", Harris: \n"
        complete_data[about_people] = complete_data[about_people] + videos[folder_name].type + str(", ") + videos[folder_name].topic + str(", ")
        complete_data[about_people] = complete_data[about_people] + videos[folder_name].direct_audience + str(", ") + videos[folder_name].other_audience + "\n"
        complete_data[about_people] = complete_data[about_people] + videos[folder_name].data_harris[about_people]

        if about_people not in data_for_analysis_harris[year]:
            data_for_analysis_harris[year][about_people] = ""
        data_for_analysis_harris[year][about_people] = data_for_analysis_harris[year][about_people] + videos[folder_name].data_harris[about_people]

#print(len(complete_data))
# for about_people in complete_data:
#     with open(str(".\data_by_about_new\\") + about_people.group + str(about_people.is_positive) + about_people.specific_topic + str(about_people.is_judging) + ".txt", "a") as file:
#         file.write(complete_data[about_people])


#     for about_people in data_for_analysis_dennett:
#         with open(str(".\data_for_emfd\\all_christians\\dennett\\") + about_people.group + str(about_people.is_positive) + about_people.specific_topic + str(about_people.is_judging) + ".txt", "a") as file:
#             file.write(data_for_analysis_dennett[about_people])

#     for about_people in data_for_analysis_Harris:
#         with open(str(".\data_for_emfd\\harris\\") + about_people.group + str(about_people.is_positive) + about_people.specific_topic + str(about_people.is_judging) + ".txt", "a") as file:
#             file.write(data_for_analysis_Harris[about_people])


#(data_for_analysis_dennett, data_for_analysis_harris, groups, folder_name, should_be_positive, is_directly):
#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_christians, "about_all_christians_directly", True, True)
#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_christians, "about_all_christians_indirectly", True, False)

#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_christians, "about_all_christians_directly_negative", False, True)
#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_christians, "about_all_christians_indirectly_negative", False, False)

#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_non_religious, "about_all_non_religious_directly", True, True)
#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_non_religious, "about_all_non_religious_indirectly", True, False)

#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_non_religious, "about_all_non_religious_directly_negative", False, True)
#save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_non_religious, "about_all_non_religious_indirectly_negative", False, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_people_in_general, "all_religious_in_general_directly", True, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_people_in_general, "all_religious_in_general_indirectly", True, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_people_in_general, "all_religious_in_general_directly_negative", False, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_people_in_general, "all_religious_in_general_indirectly_negative", False, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_muslims, "muslims_directly", True, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_muslims, "muslims_indirectly", True, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_muslims, "muslims_directly_negative", False, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_muslims, "muslims_indirectly_negative", False, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, other_religious_people, "about_other_religious_people_directly", True, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, other_religious_people, "about_other_religious_people_indirectly", True, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, other_religious_people, "about_other_religious_people_directly_negative", False, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, other_religious_people, "about_other_religious_people_indirectly_negative", False, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, christian_theologians, "about_christian_theologians_directly", True, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, christian_theologians, "about_christian_theologians_indirectly", True, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, christian_theologians, "about_christian_theologians_directly_negative", False, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, christian_theologians, "about_christian_theologians_indirectly_negative", False, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_moderates, "religious_moderates_directly", True, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_moderates, "religious_moderates_indirectly", True, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_moderates, "religious_moderates_directly_negative", False, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_moderates, "religious_moderates_indirectly_negative", False, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_fundamentalists, "religious_fundamentalists_directly", True, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_fundamentalists, "religious_fundamentalists_indirectly", True, False)

# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_fundamentalists, "religious_fundamentalists_directly_negative", False, True)
# save_filtered_data(data_for_analysis_dennett, data_for_analysis_harris, all_religious_fundamentalists, "religious_fundamentalists_indirectly_negative", False, False)

print("Dennett:", len(counts_by_types_dennett))
for about_people in counts_by_types_dennett:
    print(about_people.group, counts_by_types_dennett[about_people])


print("Harris:", len(counts_by_types_harris))
for about_people in counts_by_types_harris:
    print(about_people.group, counts_by_types_harris[about_people])


for group in religious_groups:
    print(group)

print("Video types:")

for video_type in video_types:
    print(video_type)

print("Direct audiences:")
for audience in direct_audiences:
    print(audience)
    
print("Indirect audiences:")
for audience in indirect_audiences:
    print(audience)

# print("Dennett:")
# dennett_total = 0
# for year in dennett_by_years:
#     print(year, dennett_by_years[year])
#     dennett_total = dennett_total + dennett_by_years[year]
# print("dennett_total: ", dennett_total)

# print("Harris:")
# harris_total = 0
# for year in harris_by_years:
#     print(year, harris_by_years[year])
#     harris_total = harris_total + harris_by_years[year]
# print("harris_total: ", harris_total)



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
