'''
@ author: Jan Klein
@ coop: Fraunhofer IWU

Here functions are stored which are used as helping functions for labeling squares.py

'''

import cv2

def show_window_with_user_setting(image, name, wait):
    """
    :param image:
    :param name:
    :param wait:
    :return:
    """
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 600, 600)
    cv2.imshow(name, image)
    cv2.waitKey(0)



