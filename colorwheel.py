import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mpc
from matplotlib import cm
from colorsys import rgb_to_hsv
from colours import ImageColour
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image


class ColourWheel:
    def __init__(self, skin_directory):
        """
        ColourWheel class is used to display the colourwheel with the skins put inside it
        :param skin_directory: the directory to get the skin images from, something like
                               `.../dragontail-9.17.1/img/champion`
        """
        self.ax = None
        self.generate_axis()
        self.skin_directory = skin_directory
        self.figure = plt.gcf()

    def generate_axis(self):
        """
        Generates the base axis for the colourwheel
        The figsize can be adjusted to better fit your screen.
        """
        fg = plt.figure(figsize=(15, 15))
        ax = fg.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar')
        norm = mpc.Normalize(0, 2*np.pi)
        t = np.linspace(0, 2*np.pi, 700)  # 700 seems to be a sweet spot for no obvious lines, makes a smooth wheel
        r = np.linspace(0, 1, 2)
        rg, tg = np.meshgrid(r, t)
        c = tg
        ax.pcolormesh(t, r, c.T, norm=norm, cmap=cm.get_cmap('hsv', 2056))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.spines['polar'].set_visible(True)
        self.ax = ax

    def add_data(self, skins, method='common', colours=8):
        """
        Add skins to the colourwheel.
        :param skins: Either one or a list of Skin instances
        :param method: 'common' for most common colour, 'average' for average colour
        :param colours: When method is 'common', the number of colours the image will be reduced to to find the most
                        frequent colour
        """
        if not isinstance(skins, list):
            skins = [skins]
        for skin in skins:
            if method == 'common':
                rgb = ImageColour.get_most_common(skin.get_file_path(self.skin_directory, 'loading'), colours)
            else:
                rgb = ImageColour.get_average(skin.get_file_path(self.skin_directory, 'loading'))
            h, radius, _ = rgb_to_hsv(rgb.r, rgb.g, rgb.b)
            angle = h * 2 * np.pi
            img = Image.open(skin.get_file_path(self.skin_directory, 'tiles'))
            ab = AnnotationBbox(OffsetImage(img, zoom=0.13), (angle, radius), frameon=False)
            self.ax.add_artist(ab)
        self.figure = plt.gcf()

    @staticmethod
    def show_plot():
        """
        Shows the plot
        :return:
        """
        plt.show()

    def save_plot(self, path, dpi=100):
        """
        Saves the plot
        :param dpi: DPI of the image
        :param path: the path to save the plot to
        """
        self.figure.savefig(path, dpi=dpi)
