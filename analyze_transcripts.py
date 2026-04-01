from emfdscore.scoring import score_docs 
import pandas as pd 
import numpy as np
import seaborn as sns
import os
from matplotlib import pyplot as plt

autors = ['dennett', 'harris']
for autor in autors:
    output = pd.DataFrame()
    data_folder = str('data_for_statistics/') + autor

    for file_name in os.listdir(data_folder):

        full_path = os.path.join(data_folder, file_name)
        print(full_path)
        template_input = pd.read_csv(full_path, header=None)

        template_input.head()

        num_docs = len(template_input)

        DICT_TYPE = 'emfd'
        PROB_MAP = 'single'
        SCORE_METHOD = 'bow'
        OUT_METRICS = 'sentiment'
        OUT_CSV_PATH = autor + str('2.csv')

        segment_info_raw = file_name.split('.')[0]
        segment_info = segment_info_raw.split('-')

        first_part = pd.DataFrame([[segment_info[0], segment_info[1], segment_info[2], segment_info[3], segment_info[4], segment_info[5], segment_info[6]]])
        second_part = score_docs(template_input,DICT_TYPE,PROB_MAP,SCORE_METHOD,OUT_METRICS,num_docs)
        # is not positive
        if segment_info[5] == 'False':
            second_part.loc[0,'care_sent'] *= -1
            second_part.loc[0,'fairness_sent'] *= -1
            second_part.loc[0,'loyalty_sent'] *= -1
            second_part.loc[0,'authority_sent'] *= -1
            second_part.loc[0,'sanctity_sent'] *= -1

        line_df = pd.concat([first_part, second_part], axis=1)
        output = pd.concat([output, line_df], sort=False)
        output.to_csv(OUT_CSV_PATH, index=False)
