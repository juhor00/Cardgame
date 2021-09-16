"""
Edits cards images
"""

from PIL import Image, ImageDraw
from os import listdir


class EditImage:

    def __init__(self, in_path):

        self.image = Image.open(in_path)
        self.width, self.height = self.image.size

    def crop(self, left=0, top=0, right=0, bottom=0):
        """
        Crop image from each side
        :param left: int
        :param top: int
        :param right: int
        :param bottom: int
        """

        cropped = self.image.crop((left, top, self.width-right, self.height-bottom))
        self.image = cropped

    def draw_borders(self, color, width, left=True, top=True, right=True, bottom=True):
        """
        Fill with color <width> from each border
        :param color: str
        :param width: int
        """
        draw = ImageDraw.Draw(self.image)

        if left:
            # Left border
            xy = [(0, 0), (0, self.height)]
            draw.line(xy, fill=color, width=width*2)
        if top:
            # Top border
            xy = [(0, 0), (self.width, 0)]
            draw.line(xy, fill=color, width=width * 2)
        if right:
            # Right border
            xy = [(self.width, 0), (self.width, self.height)]
            draw.line(xy, fill=color, width=width * 2)
        if bottom:
            # Bottom border
            xy = [(0, self.height), (self.width, self.height)]
            draw.line(xy, fill=color, width=width * 2)

    def save(self, out_path):
        """
        Save image
        :param out_path: str, path
        """

        self.image.save(out_path)


if __name__ == "__main__":
    path = "cards/"
    grey = "#BCBEC0"
    white = "#FFFFFF"
    for file in listdir(path):
        image = EditImage(path+file)
        image.draw_borders(white, 20)
        image.draw_borders(grey, 3)
        image.draw_borders(grey, 4, left=False)
        image.save("drawn_cards/"+file)
