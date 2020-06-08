'''
@ author: Jan Klein
@ coop: Fraunhofer IWU

This script is used to create a dataframe containing information of the tensile tests
'''

import pandas as pd

# all the following values were set after checking the pictures with the best fit circle
# see the .ods document for the origin of the values


data = {'ZP' : [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'xmin_big_d' : [23, 63, 94, 20, 33, 33, 22, 154, 31],           # minimal x-pixel values of the big diameter
        'xmax_big_d' : [526, 654, 665, 556, 482, 535,562,679,498],      # maximum x-pixel values of the big diameter
        'ymin_big_d' : [112, 41, 86, 90, 115, 50, 105, 115, 99],        # minimal y-pixel values of the big diameter
        'ymax_big_d' : [615, 632, 657, 626, 564, 552,645,640,566],      # maximum y-pixel values of the big diameter
        'img_folder_path' : ['/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP1/201315_ZP1_Bildstapel_50µm_700x746_1980bis7760/201315_ZP1_Bildstapel_50µm_700x746_1980bis7760_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP2/201315_ZP2_Bildstapel_50µm_700x746_2000bis7755/201315_ZP2_Bildstapel_50µm_700x746_2000bis7755_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP3/201315_ZP3_Bildstapel_50µm_700x746_1995bis7755/201315_ZP3_Bildstapel_50µm_700x746_1995bis7755_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP4/200113_ZP4_Bildstapel_50µm_700x746_1905bis7905/200113_ZP4_Bildstapel_50µm_700x746_1905bis7905_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP5/201315_ZP5_Bildstapel_50µm_700x746_1985bis7755/201315_ZP5_Bildstapel_50µm_700x746_1985bis7755_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP6/201315_ZP6_Bildstapel_50µm_700x746_1740bis7755/201315_ZP6_Bildstapel_50µm_700x746_1740bis7755_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP7/201315_ZP7_Bildstapel_50µm_900x746_1845bis7755/201315_ZP7_Bildstapel_50µm_900x746_1845bis7755_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP8/200124_ZP8_Bildstapel_50µm_700x746_1790bis7755/200124_ZP8_Bildstapel_50µm_700x746_1790bis7755_'
            , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP9/201315_ZP9_Bildstapel_50µm_700x746_1880bis7755/201315_ZP9_Bildstapel_50µm_700x746_1880bis7755_'],
        'min_Slice' : [396, 340, 399, 381, 397, 348, 369, 358, 376],           # lowest slice fully visible in CT
        'max_Slice' : [1551, 1491, 1551, 1551, 1551, 1551, 1551, 1551, 1551],  # highest slice fully visible in CT
        }

ZP_info = pd.DataFrame(data)

print(ZP_info)


