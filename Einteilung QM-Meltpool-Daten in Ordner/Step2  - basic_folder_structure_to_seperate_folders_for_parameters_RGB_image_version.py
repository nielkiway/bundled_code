'''
@ author: Jan Klein
@ coop: Fraunhofer IWU

Version for dealing with the RGB_images - same principle applied as before

The following code is used to move the QM-Meltpool-Data in the folder structure created in step 1 to a sub folder
structure for every parameter set:

main_folder
|- porosity             # folder for the png images labeled as porosity
|- no_porosity          # folder for the png images labeled as no porosity

to

main_folder
|- hatch_reduced
    |- porosity
    |- no_porosity
|- power_reduced
    |- porosity
    |- no_porosity
|- standard
    |- porosity
    |- no_porosity

So far the code doesn't enable the same operation for the image folder.

Via the undersampling_switch the created datasets are undersampled dataset to ensure equal numbers of examples in the
porosity and no_porosity-Subfolders
'''

import os
import random
from shutil import copyfile

random_seed = 42
num_layers = 3

undersampling_switch = False  # can be triggered to enable undersampling

# In the following section the folders need to be set. src_no_porosity is the folder filled in step 1 with all the data
# belonging to class "no porosity". The other paths are the paths of the subfolders for the different parameters
src_no_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/no_porosity'
dest_hatch_no_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/hatch_reduced/no_porosity'
dest_power_no_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/power_reduced/no_porosity'
dest_standard_no_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/standard_orig/no_porosity'

# The same procedure is repeated here for class "porosity".
src_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/porosity'
dest_hatch_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/hatch_reduced/porosity'
dest_power_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/power_reduced/porosity'
dest_standard_porosity = '/home/jan/Documents/Diplomarbeit/Code_zusammengefasst/QM-Meltpool-Datenaufbereitung/grayscale_area_images_all_slices_sorted/standard_orig/porosity'

# empty lists are initialized to store all the file names of the arrays
array_paths_porosity = []
array_paths_no_porosity = []

# listing all the file names in the folder with the no porosity arrays
for path in os.listdir(src_no_porosity):
    array_paths_no_porosity.append(path)

# empty lists are initialized for every parameter combination to store the corresponding file names
hatch_reduced_no_porosity = []
power_reduced_no_porosity = []
standard_no_porosity = []

# looping through all the file names of the no porosity arrays
for path in array_paths_no_porosity:
    zp_n = int(path[7])             # getting the number of the tensile test out of the file name
    slice_n = int(path[15:19])      # getting the slice out of the file name

    # - slices 854 to 864 are neglected as this is the region when the process was interrupted and had to be restarted
    # - tensile test 1,4 and 7 were build with reduced hatch distance from slice 776 to 875
    # - tensile test 3,6 and 9 were build with reduced power from slice 776 to 875
    # - the special area of tensile tests 2,5 and 8 are neglected because they're too porous
    # - for tensile test 2 the standard parameter area is different because of the forgotten layers at the bottom of the
    #   tensile test

    if zp_n in [1,4,7] and slice_n in range(776,876) and slice_n not in range(854,865): #876 instead of 875 because of range
        hatch_reduced_no_porosity.append(path)
    elif zp_n in [3,6,9] and slice_n in range(776,876) and slice_n not in range(854,865):
        power_reduced_no_porosity.append(path)
    elif zp_n in [1,3,4,5,6,7,8,9] and slice_n not in range(776,876):
        standard_no_porosity.append(path)
    elif zp_n == 2 and slice_n not in range(716,816) and slice_n not in range(854,865):
        standard_no_porosity.append(path)

# all the generated file name lists are randomly shuffled
random.shuffle(hatch_reduced_no_porosity)
random.shuffle(power_reduced_no_porosity)
random.shuffle(standard_no_porosity)


# doing the same for the porosity labeled data - for comments see above
for path in os.listdir(src_porosity):
    array_paths_porosity.append(path)

hatch_reduced_porosity = []
power_reduced_porosity = []
standard_porosity = []

for path in array_paths_porosity:
    zp_n = int(path[7])
    slice_n = int(path[15:19])

    if zp_n in [1,4,7] and slice_n in range(776,876) and slice_n not in range(854,865): #876 instead of 875 because of range
        hatch_reduced_porosity.append(path)
    elif zp_n in [3,6,9] and slice_n in range(776,876) and slice_n not in range(854,865):
        power_reduced_porosity.append(path)
    elif zp_n in [1,3,4,5,6,7,8,9] and slice_n not in range(776,876):
        standard_porosity.append(path)
    elif zp_n == 2 and slice_n not in range(716,816) and slice_n not in range(854,865):
        standard_porosity.append(path)

random.shuffle(hatch_reduced_porosity)
random.shuffle(power_reduced_porosity)
random.shuffle(standard_porosity)


print('done with preprocessing')

if undersampling_switch:
    # balancing the data set by just selecting the required number of data from the majority class
    # first step: comparing the lenght of the porosity list and the no-porosity list
    # The whole steps are repeated 3 times for the different parameters

    if len(hatch_reduced_no_porosity) < len(hatch_reduced_porosity):
        for path in hatch_reduced_no_porosity:
            copyfile(src_no_porosity + '/' + path, dest_hatch_no_porosity + '/' + path)
        for path in hatch_reduced_porosity[:len(hatch_reduced_no_porosity)]:
            copyfile(src_porosity + '/' + path, dest_hatch_porosity + '/' + path)

    elif len(hatch_reduced_no_porosity) > len(hatch_reduced_porosity):
        for path in hatch_reduced_no_porosity[:len(hatch_reduced_porosity)]:
            copyfile(src_no_porosity + '/' + path, dest_hatch_no_porosity + '/' + path)
        for path in hatch_reduced_porosity:
            copyfile(src_porosity + '/' + path, dest_hatch_porosity + '/' + path)

    else:
        for path in hatch_reduced_no_porosity:
            copyfile(src_no_porosity + '/' + path, dest_hatch_no_porosity + '/' + path)
        for path in hatch_reduced_porosity:
            copyfile(src_porosity + '/' + path, dest_hatch_porosity + '/' + path)

    # same steps for power reduced
    if len(power_reduced_no_porosity) < len(power_reduced_porosity):
        for path in power_reduced_no_porosity:
            copyfile(src_no_porosity + '/' + path, dest_power_no_porosity + '/' + path)
        for path in power_reduced_porosity[:len(power_reduced_no_porosity)]:
            copyfile(src_porosity + '/' + path, dest_power_porosity + '/' + path)

    elif len(power_reduced_no_porosity) > len(power_reduced_porosity):
        for path in power_reduced_no_porosity[:len(power_reduced_porosity)]:
            copyfile(src_no_porosity + '/' + path, dest_power_no_porosity + '/' + path)
        for path in power_reduced_porosity:
            copyfile(src_porosity + '/' + path, dest_power_porosity + '/' + path)

    else:
        for path in power_reduced_no_porosity:
            copyfile(src_no_porosity + '/' + path, dest_power_no_porosity + '/' + path)
        for path in power_reduced_porosity:
            copyfile(src_porosity + '/' + path, dest_power_porosity + '/' + path)

    # same steps for standard
    if len(standard_no_porosity) < len(standard_porosity):
        for path in standard_no_porosity:
            copyfile(src_no_porosity + '/' + path, dest_standard_no_porosity + '/' + path)
        for path in standard_porosity[:len(standard_no_porosity)]:
            copyfile(src_porosity + '/' + path, dest_standard_porosity + '/' + path)

    elif len(standard_no_porosity) > len(standard_porosity):
        for path in standard_no_porosity[:len(standard_porosity)]:
            copyfile(src_no_porosity + '/' + path, dest_standard_no_porosity + '/' + path)
        for path in standard_porosity:
            copyfile(src_porosity + '/' + path, dest_standard_porosity + '/' + path)

    else:
        for path in standard_no_porosity:
            copyfile(src_no_porosity + '/' + path, dest_standard_no_porosity + '/' + path)
        for path in standard_porosity:
            copyfile(src_porosity + '/' + path, dest_standard_porosity + '/' + path)

# if no balanced dataset is desired simply all the files are added to the subfolders regardless of the number of files
else:
    for path in hatch_reduced_no_porosity:
        copyfile(src_no_porosity + '/' + path, dest_hatch_no_porosity + '/' + path)
    for path in hatch_reduced_porosity:
        copyfile(src_porosity + '/' + path, dest_hatch_porosity + '/' + path)

    for path in power_reduced_no_porosity:
        copyfile(src_no_porosity + '/' + path, dest_power_no_porosity + '/' + path)
    for path in power_reduced_porosity:
        copyfile(src_porosity + '/' + path, dest_power_porosity + '/' + path)

    for path in standard_no_porosity:
        copyfile(src_no_porosity + '/' + path, dest_standard_no_porosity + '/' + path)
    for path in standard_porosity:
        copyfile(src_porosity + '/' + path, dest_standard_porosity + '/' + path)

print('done with copying')









