'''
@ author: Jan Klein
@ coop: Fraunhofer IWU

The following code is used to move the processed QM-Meltpool-Data in a folder structure with 4 sub folders:

main_folder
|- porosity             # folder for the np arrays labeled as porosity
|- no_porosity          # folder for the np arrays labeled as no porosity
|- porosity_imgs        # folder for the created images created from np arrays labeled as porosity
|- no_porosity_imgs     # folder for the created images created from np arrays labeled as no porosity

'''

import os
import pandas as pd
from shutil import copyfile


# Creating a DataFrame containing the paths to the csv files
csv_dict = {'ZP': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'csv_path': [
                '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP1/square_16_threshold_porosity_corrected_threshold=41.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP2/square_16_threshold_porosity_corrected_threshold=57.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP3/square_16_threshold_porosity_corrected_threshold=53.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP4/square_16_threshold_porosity_corrected_threshold=46.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP5/square_16_threshold_porosity_corrected_threshold=32.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP6/square_16_threshold_porosity_corrected_threshold=41.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP7/square_16_threshold_porosity_corrected_threshold=47.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP8/square_16_threshold_porosity_corrected_threshold=44.csv'
                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP9/square_16_threshold_porosity_corrected_threshold=35.csv'],
            }


# just for test purposes
#csv_dict = {'ZP': [1, 2],
#            'csv_path': [
#                '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP1/square_16_threshold_porosity_corrected_threshold=41.csv'
#                , '/home/jan/Documents/Diplomarbeit/Trainingsdaten/ZPs/ZP2/square_16_threshold_porosity_corrected_threshold=57.csv']
#            }


csv_paths = pd.DataFrame(csv_dict)


mode = 'area' # needs to be changed if intensity is selected
num_layer = 3

# Looping through all the tensile tests
for ZP_number in range(1, 10):
    print(ZP_number)        # just for debugging
    # selecting the csv path of the current tensile test and reading it in as a DataFrame
    csv_path = csv_paths[csv_paths['ZP'] == ZP_number].csv_path[ZP_number - 1]
    ZP_csv = pd.read_csv(csv_path)

    # setting the paths of the folders containing the unordered processed QM-Meltpool_data and the corresponding pictures
    array_path = '/home/jan/Documents/Diplomarbeit/Trainingsdaten/datasets_new/arrays_non_sorted/{}_layer/arrays'.format(num_layer)
    images_path = '/home/jan/Documents/Diplomarbeit/Trainingsdaten/datasets_new/arrays_non_sorted/{}_layer/imgs'.format(num_layer)

    # setting the paths of the folders of the desired folder structure (see lines 7-11)
    folder_porosity = '/home/jan/Documents/Diplomarbeit/Trainingsdaten/datasets_new/arrays_sorted_for_porosity/{}_layer/porosity'.format(num_layer)
    folder_no_porosity = '/home/jan/Documents/Diplomarbeit/Trainingsdaten/datasets_new/arrays_sorted_for_porosity/{}_layer/no_porosity'.format(num_layer)
    folder_porosity_imgs = '/home/jan/Documents/Diplomarbeit/Trainingsdaten/datasets_new/arrays_sorted_for_porosity/{}_layer/porosity_imgs'.format(num_layer)
    folder_no_porosity_imgs = '/home/jan/Documents/Diplomarbeit/Trainingsdaten/datasets_new/arrays_sorted_for_porosity/{}_layer/no_porosity_imgs'.format(num_layer)

    # looping through all the rows of the DataFrame created from the csv
    for index, row in ZP_csv.iterrows():
        # print (index) # just for debugging purposes
        # getting the information of the DataFrame
        num_slice = row['Slice']
        x = row['x-grid']
        y = row['y-grid']
        pores = row['Poren']

        # creating the array- and image-filename corresponding to the current row of the DataFrame
        src = array_path + '/' + mode + '_ZP{}_'.format(ZP_number) + 'Slice' + str("{:05d}".format(num_slice)) + '_x:' + str(
            x) + '_y:' + str(y) + '.npy'
        src_img = images_path + '/' + mode + '_ZP{}_'.format(ZP_number) + 'Slice' + str("{:05d}".format(num_slice)) + '_x:' + str(
            x) + '_y:' + str(y) + '.png'

        # checking whether the array-filename is existing - if no -> next row in DataFrame
        # The check is performed because not all the segments represented by the rows of the csv are arrays as only
        # the small diameter part of the tensile tests is of interest
        if os.path.isfile(src):
            # checking whether the segment is labeled as porous or not
            if pores == 0:
                # setting the destination folder for the array
                dst = folder_no_porosity + '/' + mode + '_ZP{}_'.format(ZP_number) + 'Slice' + str(
                    "{:05d}".format(num_slice)) + '_x:' + str(x) + '_y:' + str(y) + '.npy'
                # setting the destination folder for the image
                dst_img = folder_no_porosity_imgs + '/' + mode + '_ZP{}_'.format(ZP_number) + 'Slice' + str(
                    "{:05d}".format(num_slice)) + '_x:' + str(x) + '_y:' + str(y) + '.png'

            elif pores == 1:
                dst = folder_porosity + '/' + mode + '_ZP{}_'.format(ZP_number) + 'Slice' + str(
                    "{:05d}".format(num_slice)) + '_x:' + str(x) + '_y:' + str(y) + '.npy'

                dst_img = folder_porosity_imgs + '/' + mode + '_ZP{}_'.format(ZP_number) + 'Slice' + str(
                    "{:05d}".format(num_slice)) + '_x:' + str(x) + '_y:' + str(y) + '.png'

            # files are copied from the source folder to the desired folders
            copyfile(src, dst)
            copyfile(src_img, dst_img)

