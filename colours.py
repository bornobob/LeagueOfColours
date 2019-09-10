import numpy as np
from PIL import Image


class RGB:
    def __init__(self, r, g, b):
        """
        Simple class to save RGB colour values ([0, 255])
        :param r: R value
        :param g: G value
        :param b: B value
        """
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)


class ImageColour:
    @staticmethod
    def get_average(path):
        """
        Obtain the average RGB value of the image at the given path
        :param path: the path to the image
        :return: An instance of the RGB class
        """
        i = Image.open(path)
        i = i.convert('RGB')
        np_array = np.array(i)
        np_array = np_array.reshape((np_array.shape[0] * np_array.shape[1], np_array.shape[2]))
        return RGB(*list(np.mean(np_array, axis=0)))

    @staticmethod
    def get_most_common(path, colours=8):
        """
        Obtain the most common RGB value of the image at the given path.
        This is calculated by first reducing the image to a number of colours and then binary counting the pixels.
        :param path: the path to the image
        :param colours: the number of colours to reduce the image to before calculating summs.
        :return: An instance of the RGB class
        """
        i = Image.open(path)
        i = i.convert('P', palette=Image.ADAPTIVE, colors=colours)
        np_array = np.array(i)
        np_array = np_array.reshape((np_array.shape[0] * np_array.shape[1],))
        most_common_index = np.argmax(np.bincount(np_array))
        palette = np.array(i.getpalette()).reshape(256, 3)
        return RGB(*palette[most_common_index])
