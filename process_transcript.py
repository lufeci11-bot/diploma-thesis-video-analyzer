import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
all_non_religious = ['About atheists', 'About secular people', 'About nonreligious people', 'About scientists, secularists and atheists', 'About Christian preachers atheists']
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
    video_data.type = type_line[15:-1]
    if video_data.type not in video_types:
        video_types.append(video_data.type)

    topic_line = file.readline()
    if len(topic_line) == 0:
        print("Error in file:", folder_name)
    if not topic_line.startswith("Topic:"):
        print("Error topic_line in file:", folder_name)
    video_data.topic = topic_line[7:-1]
    if video_data.topic not in topics:
        topics.append(video_data.topic)

    direct_audience_line = file.readline()
    if len(direct_audience_line) < 3:
        print("Error in file:", folder_name)
    if not direct_audience_line.startswith("Direct audience:"):
        print("Error direct_audience_line in file:", folder_name)
    video_data.direct_audience = direct_audience_line[17:-1]
    if video_data.direct_audience not in direct_audiences:
        direct_audiences.append(video_data.direct_audience)

    other_audience_line = file.readline()
    if len(other_audience_line) < 3:
        print("Error in file:", folder_name)
    if not other_audience_line.startswith("Other audience:"):
        print("Error other_audience_line in file:", folder_name)
    video_data.other_audience = other_audience_line[16:-1]
    if video_data.other_audience not in indirect_audiences:
        indirect_audiences.append(video_data.other_audience)

    is_segment_relevant = False

    line_number = 0

    current_speaker = ""
    while True:
        line = file.readline()
        if not line:
            break
        line_tokens = line.split(' ')
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
                    for token in line_tokens:
                        if token.endswith('\n'):
                            token = token[:-1]
                        if token.endswith('\"'):
                            token = token[:-1]
                        if token.endswith('.') or token.endswith(',') or token.endswith('-'):
                            token = token[:-1]
                        #print(token)
                        video_data.data_harris[current_data_type] = video_data.data_harris[current_data_type] + token + ' '
                elif current_speaker == "Daniel Dennett":
                    if current_data_type not in video_data.data_dennett:
                        video_data.data_dennett[current_data_type] = ""
                    for token in line_tokens:
                        if token.endswith('\n'):
                            token = token[:-1]
                        if token.endswith('\"'):
                            token = token[:-1]
                        if token.endswith('.') or token.endswith(',') or token.endswith('-'):
                            token = token[:-1]
                        #print(token)
                        video_data.data_dennett[current_data_type] = video_data.data_dennett[current_data_type] + token + ' '
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
    print(folder_name)
    print(videos[folder_name].url)
    year = videos[folder_name].date.year
    if len(videos[folder_name].data_dennett) > 0 and year not in data_for_analysis_dennett:
        data_for_analysis_dennett[year] = dict()

    for about_people in videos[folder_name].data_dennett:
        if about_people not in counts_by_types_dennett:
            counts_by_types_dennett[about_people] = 0
        counts_by_types_dennett[about_people] = counts_by_types_dennett[about_people] + len(videos[folder_name].data_dennett[about_people].split())

        if about_people not in data_for_analysis_dennett[year]:
            data_for_analysis_dennett[year][about_people] = ""
        data_for_analysis_dennett[year][about_people] = data_for_analysis_dennett[year][about_people] + videos[folder_name].data_dennett[about_people]

    if len(videos[folder_name].data_harris) > 0 and year not in data_for_analysis_harris:
        data_for_analysis_harris[year] = dict()

    for about_people in videos[folder_name].data_harris:
        if about_people not in counts_by_types_harris:
            counts_by_types_harris[about_people] = 0
        counts_by_types_harris[about_people] = counts_by_types_harris[about_people] + len(videos[folder_name].data_harris[about_people].split())
        
        if about_people not in data_for_analysis_harris[year]:
            data_for_analysis_harris[year][about_people] = ""
        data_for_analysis_harris[year][about_people] = data_for_analysis_harris[year][about_people] + videos[folder_name].data_harris[about_people]

# # Years charts
# years = range(2003, 2027)

# total_by_years_dennett = dict()
# for year in years:
#     total_by_years_dennett[year] = 0

# for year in data_for_analysis_dennett:
#     for about in data_for_analysis_dennett[year]:
#         tokens = data_for_analysis_dennett[year][about].split(' ')
#         total_by_years_dennett[year] = total_by_years_dennett[year] + len(tokens)
    
# for year in years:
#     print(year, "dennett", total_by_years_dennett[year])

# total_by_years_harris = dict()
# for year in years:
#     total_by_years_harris[year] = 0
# for year in data_for_analysis_harris:
#     for about in data_for_analysis_harris[year]:
#         tokens = data_for_analysis_harris[year][about].split(' ')
#         total_by_years_harris[year] = total_by_years_harris[year] + len(tokens)

# for year in years:
#     print(year, "harris", total_by_years_harris[year])

# #plt.bar(total_by_years.keys(), total_by_years.values(), 1, color='g')

# df = pd.DataFrame({'Year': years, 'Dennett': total_by_years_dennett.values(), 'Harris': total_by_years_harris.values()})

# df.plot(x="Year", y=["Dennett", "Harris"], kind="bar")
# plt.ylabel("Words"); 
# plt.show()

# # Religious groups charts
# print("Groups: ", religious_groups)

# religious_groups= ['About Christians', 'About Christian fundamentalists', 'About moderate Christians', 'About Christian preachers', 'About Christian theologians', \
# 'About atheists', 'About nonreligious people', 'About secular people', 'About scientists, secularists and atheists', 'About scientists', 'About Christian preachers atheists', \
# 'About Muslims', 'About Muslim fundamentalists', 'About moderate Muslims', 'About other religious people', 'About religious people', 'About religious fundamentalists', 'About religious moderates']

# total_by_groups_dennett = dict()
# for group in religious_groups:
#     total_by_groups_dennett[group[6:]] = 0

# for year in data_for_analysis_dennett:
#     for about in data_for_analysis_dennett[year]:
#         tokens = data_for_analysis_dennett[year][about].split(' ')
#         print(year, about.group)
#         total_by_groups_dennett[about.group[6:]] = total_by_groups_dennett[about.group[6:]] + len(tokens)
    
# for group in total_by_groups_dennett:
#     print(group, "dennett", total_by_groups_dennett[group])

# total_by_groups_harris = dict()
# for group in religious_groups:
#     total_by_groups_harris[group[6:]] = 0

# for year in data_for_analysis_harris:
#     for about in data_for_analysis_harris[year]:
#         tokens = data_for_analysis_harris[year][about].split(' ')
#         total_by_groups_harris[about.group[6:]] = total_by_groups_harris[about.group[6:]] + len(tokens)
    
# for group in total_by_groups_harris:
#     print(group, "harris", total_by_groups_harris[group])

# print(len(religious_groups), len(total_by_groups_dennett), len(total_by_groups_harris))

# df = pd.DataFrame({'Religious groups': total_by_groups_harris.keys(), 'Dennett': total_by_groups_dennett.values(), 'Harris': total_by_groups_harris.values()})

# df.plot(x="Religious groups", y=["Dennett", "Harris"], kind="bar")
# plt.ylabel("Words"); 
# plt.show()

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

#print("Dennett:", len(counts_by_types_dennett))
#for about_people in counts_by_types_dennett:
#    print(about_people.group, counts_by_types_dennett[about_people])


#print("Harris:", len(counts_by_types_harris))
#for about_people in counts_by_types_harris:
#    print(about_people.group, counts_by_types_harris[about_people])


#for group in religious_groups:
#    print(group)

#print("Video types:")

#for video_type in video_types:
#    print(video_type)

#print("Direct audiences:")
#for audience in direct_audiences:
#    print(audience)
    
#print("Indirect audiences:")
#for audience in indirect_audiences:
#    print(audience)


# Years graph
years = range(2003, 2027)
samples_by_years_dennett = dict()
for year in years:
    samples_by_years_dennett[year] = []

samples_by_years_harris = dict()
for year in years:
    samples_by_years_harris[year] = []

religious_groups= ['About Christians', 'About Christian fundamentalists', 'About moderate Christians', 'About Christian preachers', 'About Christian theologians', \
'About atheists', 'About nonreligious people', 'About secular people', 'About scientists, secularists and atheists', 'About scientists', 'About Christian preachers atheists', \
'About Muslims', 'About Muslim fundamentalists', 'About moderate Muslims', 'About other religious people', 'About religious people', 'About religious fundamentalists', 'About religious moderates']

samples_by_groups_dennett = dict()
for group in religious_groups:
     samples_by_groups_dennett[group[6:]] = []

samples_by_groups_harris = dict()
for group in religious_groups:
     samples_by_groups_harris[group[6:]] = []

for folder_name in videos:
    for data_segment_type in videos[folder_name].data_dennett:
        year = videos[folder_name].date.year
        video_type = videos[folder_name].type
        direct_audience = videos[folder_name].direct_audience
        other_audience = videos[folder_name].other_audience
        segment_label = data_segment_type.group + "-" + str(data_segment_type.is_positive) + "-" + str(data_segment_type.is_judging)
        label = str(year) + "-" + video_type + "-" + direct_audience + "-" + other_audience + "-" + segment_label
        with open(str(".\data_for_statistics\\dennett\\") + str(label) + str(".txt"), "a") as file:
            file.write(videos[folder_name].data_dennett[data_segment_type])

        if label not in samples_by_years_dennett[year]:
            samples_by_years_dennett[year].append(label)
        if label not in samples_by_groups_dennett[data_segment_type.group[6:]]:
            samples_by_groups_dennett[data_segment_type.group[6:]].append(label)

    for data_segment_type in videos[folder_name].data_harris:
        year = videos[folder_name].date.year
        video_type = videos[folder_name].type
        direct_audience = videos[folder_name].direct_audience
        other_audience = videos[folder_name].other_audience
        segment_label = data_segment_type.group + "-" + str(data_segment_type.is_positive) + "-" + str(data_segment_type.is_judging)
        label = str(year) + "-" + video_type + "-" + direct_audience + "-" + other_audience + "-" + segment_label
        with open(str(".\data_for_statistics\\harris\\") + str(label) + str(".txt"), "a") as file:
            file.write(videos[folder_name].data_harris[data_segment_type])

        if label not in samples_by_years_harris[year]:
            samples_by_years_harris[year].append(label)
        if label not in samples_by_groups_harris[data_segment_type.group[6:]]:
            samples_by_groups_harris[data_segment_type.group[6:]].append(label)


# Years charts
samples_by_years_dennett_for_chart = dict()
for year in years:
    samples_by_years_dennett_for_chart[year] = len(samples_by_years_dennett[year])

samples_by_years_harris_for_chart = dict()
for year in years:
    samples_by_years_harris_for_chart[year] = len(samples_by_years_harris[year])

df = pd.DataFrame({'Year': years, 'Dennett': samples_by_years_dennett_for_chart.values(), 'Harris': samples_by_years_harris_for_chart.values()})

df.plot(x="Year", y=["Dennett", "Harris"], kind="bar")
plt.ylabel("Samples"); 
plt.show()

# Groupd charts
samples_by_groups_dennett_for_chart = dict()
for group in religious_groups:
    samples_by_groups_dennett_for_chart[group[6:]] = len(samples_by_groups_dennett[group[6:]])

samples_by_groups_harris_for_chart = dict()
for group in religious_groups:
    samples_by_groups_harris_for_chart[group[6:]] = len(samples_by_groups_harris[group[6:]])

df = pd.DataFrame({'Religious group': samples_by_groups_dennett_for_chart.keys(), 'Dennett': samples_by_groups_dennett_for_chart.values(), 'Harris': samples_by_groups_harris_for_chart.values()})

df.plot(x="Religious group", y=["Dennett", "Harris"], kind="bar")
plt.ylabel("Samples"); 
plt.show()

#Excel filters - direct comparison
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers")))
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About moderate Christians")+(E2:E161="About Christian theologians")))

# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About atheists")+(E2:E161="About nonreligious people")+(E2:E161="About Christian preachers atheists")))
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About scientists, secularists and atheists")+(E2:E161="About secular people")))
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About Christian preachers atheists")))

#Excel filters - all comparison
# All Christians
# =FILTER(E2:Q161, (E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers"))
# =FILTER(E2:Q161, (E2:E161="About moderate Christians")+(E2:E161="About Christian theologians"))

# All Atheists
# =FILTER(E2:Q161, (E2:E161="About atheists")+(E2:E161="About nonreligious people")+(E2:E161="About Christian preachers atheists"))
# =FILTER(E2:Q161, (E2:E161="About scientists, secularists and atheists")+(E2:E161="About secular people"))
# =FILTER(E2:Q161, (E2:E161="About Christian preachers atheists"))

# All Atheists - nonreligious
# =FILTER(E2:Q161, (E2:E161="About atheists"))

# =FILTER(E2:Q161, (E2:E161="About nonreligious people")+(E2:E161="About Christian preachers atheists"))
# =FILTER(E2:Q161, (E2:E161="About scientists, secularists and atheists")+(E2:E161="About secular people"))

#Scientists
# Scientists
# =FILTER(E2:Q161, (E2:E161="About scientists"))

#Excel filters - all comparison
# Christians commoners
# =FILTER(E2:Q161, (E2:E161="About moderate Christians")+(E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers"))
# Christian theologians
# =FILTER(E2:Q161, (E2:E161="About Christian theologians"))

# Other religious groups
# =FILTER(E2:Q161, (E2:E161="About Muslims")+(E2:E161="About moderate Muslims")+(E2:E161="About Muslim fundamentalists")+(E2:E161="About other religious people"))
#
# Filter Muslims
# =FILTER(E2:Q161, (E2:E161="About Muslims")+(E2:E161="About moderate Muslims")+(E2:E161="About Muslim fundamentalists"))

# Filter all religious people
# =FILTER(E2:Q161, (E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers"))
# =FILTER(E2:Q161, (E2:E161="About moderate Christians")+(E2:E161="About Christian theologians"))
# =FILTER(E2:Q161, (E2:E161="About Muslims")+(E2:E161="About moderate Muslims")+(E2:E161="About Muslim fundamentalists")+(E2:E161="About other religious people"))
# =FILTER(E2:Q161, (E2:E161="About religious people")+(E2:E161="About religious fundamentalists")+(E2:E161="About religious moderates"))

# Filter all religious people direct
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers")))
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About moderate Christians")+(E2:E161="About Christian theologians")))
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About Muslims")+(E2:E161="About moderate Muslims")+(E2:E161="About Muslim fundamentalists")+(E2:E161="About other religious people")))
# =FILTER(E2:Q161, (G2:G161=TRUE)*((E2:E161="About religious people")+(E2:E161="About religious fundamentalists")+(E2:E161="About religious moderates")))

# Religious fundamentalists
# =FILTER(E2:Q161, (E2:E161="About religious fundamentalists")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Muslim fundamentalists"))

# Religious moderates
# =FILTER(E2:Q161, (E2:E161="About moderate Christians")+(E2:E161="About moderate Muslims")+(E2:E161="About religious moderates"))

# All the Christians for anova
# =FILTER(A2:Q161, (E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers"))
# =FILTER(A2:Q161, (E2:E161="About moderate Christians")+(E2:E161="About Christian theologians"))

# All the atheists for anova
# =FILTER(A2:Q161, (E2:E161="About atheists")+(E2:E161="About nonreligious people")+(E2:E161="About Christian preachers atheists"))
# =FILTER(A2:Q161, (E2:E161="About scientists, secularists and atheists")+(E2:E161="About secular people"))

# All the religious people for anova
# =FILTER(A2:Q161, (E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers"))
# =FILTER(A2:Q161, (E2:E161="About moderate Christians")+(E2:E161="About Christian theologians"))
# =FILTER(A2:Q161, (E2:E161="About Muslims")+(E2:E161="About moderate Muslims")+(E2:E161="About Muslim fundamentalists")+(E2:E161="About other religious people"))
# =FILTER(A2:Q161, (E2:E161="About religious people")+(E2:E161="About religious fundamentalists")+(E2:E161="About religious moderates"))

# scientists for anova
# =FILTER(A2:Q161, (E2:E161="About scientists"))

# Direct Christians for anova
# =FILTER(A2:Q161, (G2:G161=TRUE)*((E2:E161="About Christians")+(E2:E161="About Christian fundamentalists")+(E2:E161="About Christian preachers")))
# =FILTER(A2:Q161, (G2:G161=TRUE)*((E2:E161="About moderate Christians")+(E2:E161="About Christian theologians")))





#For Harris

#Excel filters - direct comparison
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers")))
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About moderate Christians")+(E2:E212="About Christian theologians")))

# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About atheists")+(E2:E212="About nonreligious people")+(E2:E212="About Christian preachers atheists")))
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About scientists, secularists and atheists")+(E2:E212="About secular people")))
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About Christian preachers atheists")))

#Excel filters - all comparison
# All Christians
# =FILTER(E2:Q212, (E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers"))
# =FILTER(E2:Q212, (E2:E212="About moderate Christians")+(E2:E212="About Christian theologians"))

# All Atheists
# =FILTER(E2:Q212, (E2:E212="About atheists")+(E2:E212="About nonreligious people")+(E2:E212="About Christian preachers atheists"))
# =FILTER(E2:Q212, (E2:E212="About scientists, secularists and atheists")+(E2:E212="About secular people"))
# =FILTER(E2:Q212, (E2:E212="About Christian preachers atheists"))


# All Atheists
# =FILTER(E2:Q212, (E2:E212="About atheists"))

# =FILTER(E2:Q212, (E2:E212="About nonreligious people")+(E2:E212="About Christian preachers atheists"))
# =FILTER(E2:Q212, (E2:E212="About scientists, secularists and atheists")+(E2:E212="About secular people"))

# =FILTER(E2:Q212, (E2:E212="About Christian preachers atheists"))

#Scientists
# Scientists
# =FILTER(E2:Q212, (E2:E212="About scientists"))

#Excel filters - all comparison
# Christians commoners
# =FILTER(E2:Q212, (E2:E212="About moderate Christians")+(E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers"))
# Christian theologians
# =FILTER(E2:Q212, (E2:E212="About Christian theologians"))

# Other religious groups
# =FILTER(E2:Q212, (E2:E212="About Muslims")+(E2:E212="About moderate Muslims")+(E2:E212="About Muslim fundamentalists")+(E2:E212="About other religious people"))
#
# Filter Muslims
# =FILTER(E2:Q212, (E2:E212="About Muslims")+(E2:E212="About moderate Muslims")+(E2:E212="About Muslim fundamentalists"))

# Filter all religious people
# =FILTER(E2:Q212, (E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers"))
# =FILTER(E2:Q212, (E2:E212="About moderate Christians")+(E2:E212="About Christian theologians"))
# =FILTER(E2:Q212, (E2:E212="About Muslims")+(E2:E212="About moderate Muslims")+(E2:E212="About Muslim fundamentalists")+(E2:E212="About other religious people"))
# =FILTER(E2:Q212, (E2:E212="About religious people")+(E2:E212="About religious fundamentalists")+(E2:E212="About religious moderates"))

# Filter all religious people direct
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers")))
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About moderate Christians")+(E2:E212="About Christian theologians")))
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About Muslims")+(E2:E212="About moderate Muslims")+(E2:E212="About Muslim fundamentalists")+(E2:E212="About other religious people")))
# =FILTER(E2:Q212, (G2:G212=TRUE)*((E2:E212="About religious people")+(E2:E212="About religious fundamentalists")+(E2:E212="About religious moderates")))

# Religious fundamentalists
# =FILTER(E2:Q212, (E2:E212="About religious fundamentalists")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Muslim fundamentalists"))
# Christian fundamentalists
# =FILTER(E2:Q212, (E2:E212="About Christian fundamentalists"))
# The rest of Christians
# =FILTER(E2:Q212, (E2:E212="About Christians")+(E2:E212="About Christian preachers"))
# =FILTER(E2:Q212, (E2:E212="About moderate Christians")+(E2:E212="About Christian theologians"))
# The rest of all relgious
# =FILTER(E2:Q212, (E2:E212="About Muslims")+(E2:E212="About moderate Muslims")+(E2:E212="About other religious people"))
# =FILTER(E2:Q212, (E2:E212="About religious people")+(E2:E212="About religious moderates"))

# Religious moderates
# =FILTER(E2:Q212, (E2:E212="About moderate Christians")+(E2:E212="About moderate Muslims")+(E2:E212="About religious moderates"))

# All the Christians for anova
# =FILTER(A2:Q212, (E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers"))
# =FILTER(A2:Q212, (E2:E212="About moderate Christians")+(E2:E212="About Christian theologians"))

# All the atheists for anova
# =FILTER(A2:Q212, (E2:E212="About atheists")+(E2:E212="About nonreligious people")+(E2:E212="About Christian preachers atheists"))
# =FILTER(A2:Q212, (E2:E212="About scientists, secularists and atheists")+(E2:E212="About secular people"))

# All the religious people for anova
# =FILTER(A2:Q212, (E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers"))
# =FILTER(A2:Q212, (E2:E212="About moderate Christians")+(E2:E212="About Christian theologians"))
# =FILTER(A2:Q212, (E2:E212="About Muslims")+(E2:E212="About moderate Muslims")+(E2:E212="About Muslim fundamentalists")+(E2:E212="About other religious people"))
# =FILTER(A2:Q212, (E2:E212="About religious people")+(E2:E212="About religious fundamentalists")+(E2:E212="About religious moderates"))

# scientists for anova
# =FILTER(A2:Q212, (E2:E212="About scientists"))

# Direct Christians for anova
# =FILTER(A2:Q212, (G2:G212=TRUE)*((E2:E212="About Christians")+(E2:E212="About Christian fundamentalists")+(E2:E212="About Christian preachers")))
# =FILTER(A2:Q212, (G2:G212=TRUE)*((E2:E212="About moderate Christians")+(E2:E212="About Christian theologians")))