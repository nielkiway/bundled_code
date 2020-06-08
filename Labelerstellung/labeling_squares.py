'''
@ author: Jan Klein
@ coop: Fraunhofer IWU

This Script is designed to automatically create a csv containing labels needed for generating labeled data sets
'''

import cv2
from helping_functions import show_window_with_user_setting
from ZP_info import ZP_info
import numpy as np
import math
import pandas as pd
import sys

show_images = False
show_label_generation = False
save_ct_images = True


# general settings
threshold_binary = 120          # selected threshold used for creating binary images from greyscale images
grid_size_in_bit = 880          # grid size in QM-Meltpool-Bit (derived from the Meltpool-Data processing)
max_diameter_bit = 1748         # maximum diameter of the tensile tests used for the study in QM-Meltpool-Bit
bit_µm_ratio = 0.252            # Bit/µm - the value was derived from pre investigations at IWU
equivalent_pore_diameter = 100  # µm threshold calculation depends just on this value
num_grid_x = 1                  # number of grids in x direction
num_grid_y = 1                  # number of grids in y direction


for number_zp in range(1,10):
    # print(number_zp)
    # getting the values form ZP_info belonging to the desired tensile test
    xmin_big_d = ZP_info[ZP_info.ZP == number_zp].xmin_big_d[number_zp-1]
    xmax_big_d = ZP_info[ZP_info.ZP == number_zp].xmax_big_d[number_zp-1]
    ymin_big_d = ZP_info[ZP_info.ZP == number_zp].ymin_big_d[number_zp-1]
    ymax_big_d = ZP_info[ZP_info.ZP == number_zp].ymax_big_d[number_zp-1]
    img_folder_path = ZP_info[ZP_info.ZP == number_zp].img_folder_path[number_zp-1]
    min_Slice = ZP_info[ZP_info.ZP == number_zp].min_Slice[number_zp-1]
    max_Slice = ZP_info[ZP_info.ZP == number_zp].max_Slice[number_zp-1]


    # basic calculations
    max_diameter_pixel = xmax_big_d-xmin_big_d
    max_diameter_µm = max_diameter_bit/bit_µm_ratio

    max_diameter_small_circle_pixel = max_diameter_pixel * 0.72
    # 0.72 is the ratio betw. the big diam. circle and the small one
    square_length_pixel = 0.7 * max_diameter_small_circle_pixel
    # 0.7 comes from pythagoras when fitting the square in the circle (rounded down from 0.7 to not have issues
    # with borders)
    grid_size_in_pixel = int(square_length_pixel / num_grid_x)

    # absolute threshold calculation based on absolute area
    µm_pixel_ratio = max_diameter_µm/max_diameter_pixel  # ratio between µm and side length of a pixel
    area_per_pixel = µm_pixel_ratio*µm_pixel_ratio  # area per pixel element [µm²]
    pore_area_µm = math.pi*0.25*equivalent_pore_diameter*equivalent_pore_diameter  # area of pore depending on pore diameter [µm²]
    threshold_porosity_abs = int(pore_area_µm/area_per_pixel) # rounded down number of pixels needed to form the area of pore

    print('grid_size_in_pixel: '+str(grid_size_in_pixel))
    print('µm_pixel_ratio: '+str(µm_pixel_ratio))
    print('area_per_pixel: '+str(area_per_pixel))
    print('max_diameter_µm: '+str(max_diameter_µm))
    print('pore_area_µm: '+str(pore_area_µm))
    print('threshold_porosity_abs: '+str(threshold_porosity_abs))

    # file paths - need to be adjusted due to desired locations
    csv_file_path = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/Labelerstellung/csv_files/ZP{}_threshold={}.csv'.format(number_zp, threshold_porosity_abs)
    CT_cut_path_pores = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/Labelerstellung/CT_imgs/porosity_imgs'
    CT_cut_path_no_pores = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/Labelerstellung/CT_imgs/no_porosity_imgs'


    # sys.exit()  # just for debugging

    # calculating the minimal and maximal x and y values of the cutout square
    xmin = int(xmin_big_d + 0.5*(max_diameter_pixel-square_length_pixel))
    xmax = int(xmin + square_length_pixel)
    ymin = int(ymin_big_d + 0.5*(max_diameter_pixel-square_length_pixel))
    ymax = int(ymin + square_length_pixel)

    # calculating the total number of slices
    number_slices_total = max_Slice-min_Slice

    # initializing an empty array for storing the label information
    label_storage_array = np.empty([0, 5], dtype=int)


    # start looping through all slices
    # looping with range(number_slices_total) because the images were automatically saved with an ending starting from 0
    # and counting up when exporting the images from VGStudioMax

    for img_number in range(number_slices_total):

        # current image is selected
        cur_img_path = img_folder_path+'{:04d}.tif'.format(img_number)

        # image is read in as RGB and greyscale image
        img = cv2.imread(cur_img_path)
        gray = cv2.imread(cur_img_path, cv2.IMREAD_GRAYSCALE)

        # both images are cut to the square fitting in the small diameter circle
        cut_image_rgb = img[ymin:ymax, xmin:xmax]
        cut_image = gray[ymin:ymax, xmin:xmax]

        height = cut_image.shape[0]
        width = cut_image.shape[1]

        # for visualization purposes the raw image is cut to the big diameter
        cut_image_rgb_big_diameter = img[ymin_big_d:ymax_big_d, xmin_big_d:xmax_big_d]

        if show_images:
            show_window_with_user_setting(cut_image_rgb_big_diameter, 'image big d', 0)
            show_window_with_user_setting(cut_image_rgb, 'image cut', 0)

        # getting a binary image
        _, thresh = cv2.threshold(cut_image, threshold_binary, 255, 0)

        if show_images:
            show_window_with_user_setting(thresh, 'thresh', 0)

        # getting a copy of the binary image for visualization
        grid_display_picture = np.copy(thresh)

        # The following code is used for segmenting and counting the black pixel values of each segment and thereby labeling
        # the segments. The label information is stored in a csv file which is later used to process the QM-Meltpool-Data
        # to a folder structure.

        # first an empty array is created
        check_array = np.empty([0, 5], dtype=int)

        # looping through all the possible grid combinations
        for j in range(num_grid_x):
            for i in range(num_grid_y):

                # selecting the area of the binary image belonging to the current grid
                cur_image = thresh[i * grid_size_in_pixel:(i + 1) * grid_size_in_pixel,
                            j * grid_size_in_pixel:(j + 1) * grid_size_in_pixel]

                # creating a cutout of the greyscale image belonging to the current grid (just for visualization purposes)
                cur_image_save = cut_image[i * grid_size_in_pixel:(i + 1) * grid_size_in_pixel,
                            j * grid_size_in_pixel:(j + 1) * grid_size_in_pixel]

                # adding a rectangle representing the current grid on top of the binary image (just for visualization
                # purposes)
                cur_cutout = cv2.rectangle(grid_display_picture, (j * grid_size_in_pixel, i * grid_size_in_pixel),
                                           ((j + 1) * grid_size_in_pixel, (i + 1) * grid_size_in_pixel), 0, 1)

                if show_label_generation:
                    show_window_with_user_setting(cur_cutout, 'cutout_image', 0)
                    show_window_with_user_setting(cur_image, 'cur_image', 0)
                    show_window_with_user_setting(cur_image_save, 'cur image save',0)

                # here the total number of pixels of the grid is calculated and the number of white pixels substracted to
                # get the total number of black pixels of the grid
                total_num_pixels = cur_image.shape[0]*cur_image.shape[1]
                num_black_pixels = total_num_pixels - cv2.countNonZero(cur_image)

                if show_label_generation:
                    print('x: ' + str(j))
                    print('y: ' + str(i))
                    print(num_black_pixels)

                # here the label is created by comparing the number of black pixels to the predefined threshold
                if num_black_pixels >= threshold_porosity_abs:
                    text_1 = 1  # code for black is inside

                    if save_ct_images:
                        cv2.imwrite(CT_cut_path_pores + '/Gridsize_{}_ZP{}_Slice{}_x{}_y{}.png'.format(grid_size_in_bit,
                                                                                                 number_zp,
                                                                                                 img_number + min_Slice, j,
                                                                                                 i),
                                    cur_image_save)
                else:
                    text_1 = 0  # code for no black is inside
                    if save_ct_images:
                        cv2.imwrite(CT_cut_path_no_pores + '/Gridsize_{}_ZP{}_Slice{}_x{}_y{}.png'.format(grid_size_in_bit,
                                                                                                 number_zp,
                                                                                                 img_number + min_Slice, j,
                                                                                                 i),
                                    cur_image_save)

                # the information of the current slice, current grid number in x and y direction as well as the porosity
                # label and number of black pixels (for further investigations) is stored
                # (img_number + min_slice is the current slice number
                cur_arr = np.stack((img_number+min_Slice, j, i,  text_1, num_black_pixels), axis=-1)

                print(str(img_number+min_Slice))
                check_array = np.vstack((check_array, cur_arr))

        # adding the check array to the label storage array
        label_storage_array = np.vstack((label_storage_array, check_array))


    # creating a pandas DataFrame from label_storage_array and exporting the DataFrame to the desired csv
    label_df = pd.DataFrame(data = label_storage_array, columns=(['Slice', 'x-grid', 'y-grid', 'Poren', 'num Black pixels']))
    label_df.to_csv(csv_file_path)
    print('done with ZP' + str(number_zp))