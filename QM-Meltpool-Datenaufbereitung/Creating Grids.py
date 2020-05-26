'''
@ coop: Fraunhofer IWU
@ author: Jan Klein

The following code is used to generate the segments with QM-Meltpool-Data of just 1 layer or 3 layers in grid structure
'''

from helping_functions import get_min_max_values_xy_selected_slices, getting_2D_data_from_h5_filtered_np_xy_switched, dock_array_to_zero, create_single_grid_array, process_data_to_picturelike_structure
from slice_information import slice_numbers
import numpy as np
from PIL import Image


intensity_limit = 1750
kernel_size = 5
n_grid_x, n_grid_y = 4, 4    # needs to be changed for different segmentation strategy
Multilayer = False  # needs to be switched to True if the surrounding layers should be added

for ZP_number in range(1,10):
    # general calculations
    h5_path = '/home/jan/Documents/Trainingsdaten/ZPs/ZP{}/ZP_{}_full_part.h5'.format(ZP_number, ZP_number)
    part_name = 'ZP{}_combined'.format(ZP_number)
    max_slice = slice_numbers.at[ZP_number-1, 'maxSlice']
    min_slice = slice_numbers.at[ZP_number-1, 'minSlice']
    minX, minY, maxX, maxY = get_min_max_values_xy_selected_slices(h5_path, part_name, min_slice_num = min_slice, max_slice_num = max_slice, intensity_limit= intensity_limit)

    length_x_part = maxX - minX
    length_y_part = maxY - minY

    min_square = int(0.15*length_x_part)  # 0.15 and 0.85 are derived from pythagoras and sqrt of 2 when cutting the square out of the circle
    max_square = int(0.85*length_x_part)

    y_max = max_square-min_square
    grid_size = int(y_max/4)
    print('grid_size = ' + str(grid_size))
    print('preprocesses successfully finished')

    for num_slice in range(min_slice, max_slice+1):
        print(num_slice)
        slice_name = 'Slice' + str("{:05d}".format(num_slice))
        array_filtered_not_docked = getting_2D_data_from_h5_filtered_np_xy_switched(h5_path, part_name, slice_name, intensity_limit, show_info=False)
        array_filtered_docked = dock_array_to_zero(array_filtered_not_docked, minX, minY)

        if Multilayer:
            slice_name_below = 'Slice' + str("{:05d}".format(num_slice-1))
            slice_name_above = 'Slice' + str("{:05d}".format(num_slice+1))

            array_filtered_not_docked_below = getting_2D_data_from_h5_filtered_np_xy_switched(h5_path, part_name,
                                                                                              slice_name_below,
                                                                                              intensity_limit,
                                                                                              show_info=False)
            array_filtered_docked_below = dock_array_to_zero(array_filtered_not_docked_below, minX, minY)

            array_filtered_not_docked_above = getting_2D_data_from_h5_filtered_np_xy_switched(h5_path, part_name,
                                                                                              slice_name_above,
                                                                                              intensity_limit,
                                                                                              show_info=False)
            array_filtered_docked_above = dock_array_to_zero(array_filtered_not_docked_above, minX, minY)

        # until here an array containing a circle which is coordinate-wise docked to zero at the left bottom corner is
        # created the following lines of code cut away the roundings of the circle and return a square centered in the
        # middle of the former circle

        # finding all the entries in the array which exceed the square and concatenating to one array
        x_min_cut = np.where(array_filtered_docked[:, 0] < min_square)
        x_max_cut = np.where(array_filtered_docked[:, 0] > max_square)
        y_min_cut = np.where(array_filtered_docked[:, 1] < min_square)
        y_max_cut = np.where(array_filtered_docked[:, 1] > max_square)
        cut = np.concatenate((x_min_cut, x_max_cut, y_min_cut, y_max_cut), axis=1, out=None)

        if Multilayer:
            x_min_cut_below = np.where(array_filtered_docked_below[:, 0] < min_square)
            x_max_cut_below = np.where(array_filtered_docked_below[:, 0] > max_square)
            y_min_cut_below = np.where(array_filtered_docked_below[:, 1] < min_square)
            y_max_cut_below = np.where(array_filtered_docked_below[:, 1] > max_square)
            cut_below = np.concatenate((x_min_cut_below, x_max_cut_below, y_min_cut_below, y_max_cut_below), axis=1, out=None)

            x_min_cut_above = np.where(array_filtered_docked_above[:, 0] < min_square)
            x_max_cut_above = np.where(array_filtered_docked_above[:, 0] > max_square)
            y_min_cut_above = np.where(array_filtered_docked_above[:, 1] < min_square)
            y_max_cut_above = np.where(array_filtered_docked_above[:, 1] > max_square)
            cut_above = np.concatenate((x_min_cut_above, x_max_cut_above, y_min_cut_above, y_max_cut_above), axis=1, out=None)

        # deleting all those entries --> leaving over a square shaped array
        square_filtered = np.delete(array_filtered_docked, cut, axis=0)

        if Multilayer:
            square_filtered_below = np.delete(array_filtered_docked_below, cut_below, axis=0)
            square_filtered_above = np.delete(array_filtered_docked_above, cut_above, axis=0)

        # docking the square shaped array to zero by substracting the minimal x and y value
        square_filtered[:, 0] -= min_square
        square_filtered[:, 1] -= min_square

        if Multilayer:
            square_filtered_below[:, 0] -= min_square
            square_filtered_below[:, 1] -= min_square
            square_filtered_above[:, 0] -= min_square
            square_filtered_above[:, 1] -= min_square

        # iterating through every grid
        if Multilayer:
            for cur_n_grid_x in range(n_grid_x):
                for cur_n_grid_y in range(n_grid_y):
                    final_array = create_single_grid_array(cur_n_grid_x, cur_n_grid_y, grid_size, square_filtered, y_max)
                    final_grid = process_data_to_picturelike_structure(final_array, grid_size, kernel_size, intensity_limit)

                    final_array_below = create_single_grid_array(cur_n_grid_x, cur_n_grid_y, grid_size, square_filtered_below, y_max)
                    final_grid_below = process_data_to_picturelike_structure(final_array_below, grid_size, kernel_size, intensity_limit)

                    final_array_above = create_single_grid_array(cur_n_grid_x, cur_n_grid_y, grid_size, square_filtered_above, y_max)
                    final_grid_above = process_data_to_picturelike_structure(final_array_above, grid_size, kernel_size, intensity_limit)

                    three_layer_data = np.zeros((grid_size, grid_size, 3), dtype=np.uint8)

                    for i in range(grid_size):
                        for j in range(grid_size):
                            three_layer_data[i][j][0] = final_grid_below[i][j]
                            three_layer_data[i][j][1] = final_grid[i][j]
                            three_layer_data[i][j][2] = final_grid_above[i][j]
                    np.save('/home/jan/Desktop/TryOut/ZP{}_{}_x:{}_y:{}'.format(ZP_number,slice_name, cur_n_grid_x, cur_n_grid_y),three_layer_data)
                    img = Image.fromarray(three_layer_data)
                    img.save('/home/jan/Desktop/TryOut/imgs/ZP{}_{}_x:{}_y:{}'.format(ZP_number, slice_name, cur_n_grid_x, cur_n_grid_y) + '.png')

        else:
            for cur_n_grid_x in range(n_grid_x):
                for cur_n_grid_y in range(n_grid_y):
                    final_array = create_single_grid_array(cur_n_grid_x, cur_n_grid_y, grid_size, square_filtered,
                                                           y_max)
                    final_grid = process_data_to_picturelike_structure(final_array, grid_size, kernel_size,
                                                                       intensity_limit)
                    # saving the picture
                    np.save('/home/jan/Desktop/TryOut/ZP{}_{}_x:{}_y:{}'.format(ZP_number, slice_name, cur_n_grid_x,
                                                                                cur_n_grid_y), final_grid)
                    img = Image.fromarray(final_grid)
                    img.save(
                        '/home/jan/Desktop/TryOut/imgs/ZP{}_{}_x:{}_y:{}'.format(ZP_number, slice_name, cur_n_grid_x,
                                                                                 cur_n_grid_y) + '.png')

print('done with ZP{}'.format(ZP_number))