'''
This script is just used to store information about the minimum and maximum slices of interest - in this case its the
slice numbers of the sections with small diameters
'''

import pandas as pd

# just for tryout
#data = {'ZP' : [1,2,3,4,5,6,7,8,9],
#        'minSlice' : [776, 467, 527, 527, 527, 527, 527, 527, 527],
#        'maxSlice' : [875, 468, 528, 528, 528, 528,528,528,528]}

#data = {'ZP' : [1,2,3,4,5,6,7,8,9],
#        'minSlice' : [527, 467, 527, 527, 527, 527, 527, 527, 527],
#        'maxSlice' : [1126, 1066, 1126, 1126, 1126, 1126,1126,1126,1126]}

data = {'ZP': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'minSlice': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'maxSlice': [1590, 1530, 1590, 1590, 1590, 1590, 1590, 1590, 1590]}

slice_numbers = pd.DataFrame(data)

