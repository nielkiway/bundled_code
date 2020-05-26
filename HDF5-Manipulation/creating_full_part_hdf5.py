'''
@ author: Jan Klein
@ coop: Fraunhofer IWU

The follwing script is used to generate one HDF5 database  for each tensile test without empty slices
'''

import h5py
import math
import re


# Path of the original HDF5 database of the whole buildjob
path_buildjob_hdf5 = '/media/jan/TOSHIBA EXT/other stuff/Sicherung_Ubuntu/Klein_Datentransfer/HDF/BJ_Superlativ_QualiPro.h5'

# The following lines contain the names of parts in the original hdf5-File of the buildjob
# ..Z_cls represents the Standard Parameter section, P_.._cls represents the special parameter section
ZP1_z = '0_00097_ZP1_Z_cls'
ZP1_p = '0_00099_ZP1_P_3_cls'

ZP2_z = '0_00093_ZP2_Z_cls'
ZP2_p = '0_00095_ZP2_P_6_cls'

ZP3_z = '0_00089_ZP3_Z_cls'
ZP3_p = '0_00090_ZP3_P_9_cls'

ZP4_z = '0_00109_ZP4_Z_cls'
ZP4_p = '0_00110_ZP4_P_2_cls'

ZP5_z = '0_00105_ZP5_Z_cls'
ZP5_p = '0_00106_ZP5_P_5_cls'

ZP6_z = '0_00101_ZP6_Z_cls'
ZP6_p = '0_00103_ZP6_P_8_cls'

ZP7_z = '0_00122_ZP7_Z_cls'
ZP7_p = '0_00123_ZP7_P_cls'

ZP8_z = '0_00117_ZP8_Z_cls'
ZP8_p = '0_00118_ZP8_P_4_cls'

ZP9_z = '0_00113_ZP9_Z_cls'
ZP9_p = '0_00114_ZP9_P_7_cls'

# here the number of the tensile test needs to be specified, the names of the two parts in the buildjob representing
# the tensile test need to be set manually. Could have been solved with a for loop with a dict but wasn't necessary
number = 1
buildjob_name_z = ZP1_z
buildjob_name_p = ZP1_p

new_file_path = '/home/jan/Desktop//ZP_{}_full_part.h5'.format(number, number)
name_in_h5 = 'ZP{}_combined'.format(number)


# searching for all the slices which contain information in the standard parameter part
list_z_param = []
with h5py.File(path_buildjob_hdf5, 'a') as h5:
    key_list = h5[buildjob_name_z].keys()       # here all the slices are listed

    for key in key_list:                        # here only the slices which contain content are added to another list
        # shape suchen
        shape = h5[buildjob_name_z][key]['Area'].shape[0]
        # Area value was just randomly chosen - wouldn't make a difference if it was the x,y position or intensity
        if shape > 0:
            list_z_param.append(key)
    print(list_z_param)


# searching for all the slices which contain information in the special parameter part
# same procedure as in the code block above - therefor not commented again
list_p_param = []
with h5py.File(path_buildjob_hdf5, 'a') as h5:
    key_list = h5[buildjob_name_p].keys()

    for key in key_list:
        shape = h5[buildjob_name_p][key]['Area'].shape[0]
        if shape > 0:
            list_p_param.append(key)
    print(list_p_param)


# the following code transfers the created lists with slices containing information in a new hdf5 part
# empty hdf5 file with writing permission is created first
Training_hdf = h5py.File(new_file_path, "w")
Training_hdf.close()

with h5py.File(new_file_path, 'a') as h5:
    # new group representing the part is created
    h5.create_group(name_in_h5)

    # the following for block adds all the slices of the list with standard parameters
    for slice_num in list_z_param:
        # the following block transforms the uneven layer numbers in normal numbers
        slice_num_int = int(re.search(r'\d+', slice_num).group())
        slice_num_normal = math.trunc(slice_num_int / 2)
        slice_name_normal = 'Slice' + str("{:05d}".format(slice_num_normal))

        # for every new slice name the information of the corresponding "old" slice is transferred
        h5[name_in_h5].create_group(slice_name_normal)
        with h5py.File(path_buildjob_hdf5, 'a') as h5_2:
            h5[name_in_h5][slice_name_normal].create_dataset('Area', data=h5_2[buildjob_name_z][slice_num]['Area'])
            h5[name_in_h5][slice_name_normal].create_dataset('Intensity',
                                                             data=h5_2[buildjob_name_z][slice_num]['Intensity'])
            h5[name_in_h5][slice_name_normal].create_dataset('X-Axis',
                                                             data=h5_2[buildjob_name_z][slice_num]['X-Axis'])
            h5[name_in_h5][slice_name_normal].create_dataset('Y-Axis',
                                                             data=h5_2[buildjob_name_z][slice_num]['Y-Axis'])

    # the following for block repeats the same for the special parameters
    for slice_num in list_p_param:
        # the following block transforms the uneven layer numbers in normal numbers
        slice_num_int_p = int(re.search(r'\d+', slice_num).group())
        slice_num_normal_p = math.trunc(slice_num_int_p / 2)
        slice_name_normal_p = 'Slice' + str("{:05d}".format(slice_num_normal_p))

        h5[name_in_h5].create_group(slice_name_normal_p)
        with h5py.File(path_buildjob_hdf5, 'a') as h5_2:
            h5[name_in_h5][slice_name_normal_p].create_dataset('Area', data=h5_2[buildjob_name_p][slice_num]['Area'])
            h5[name_in_h5][slice_name_normal_p].create_dataset('Intensity',
                                                               data=h5_2[buildjob_name_p][slice_num]['Intensity'])
            h5[name_in_h5][slice_name_normal_p].create_dataset('X-Axis',
                                                               data=h5_2[buildjob_name_p][slice_num]['X-Axis'])
            h5[name_in_h5][slice_name_normal_p].create_dataset('Y-Axis',
                                                               data=h5_2[buildjob_name_p][slice_num]['Y-Axis'])
print('done with ZP{}'.format(number))