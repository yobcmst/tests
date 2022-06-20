import abc
import cv2
import pydicom

class ImageFormat(abc.ABC):
    def __init__(self, filename: str):
        self.filename = filename
        self._image = None

    @abc.abstractmethod
    def read(self):
        ...
    
    @property
    def image(self):
        return self.get_image()

    def get_image(self):
        if self._image is not None:
            return self._image
        return self.read()

    @property
    def shape(self):
        return self.image.shape

class Png(ImageFormat):
    def read(self):
        return cv2.imread(self.filename)

class Jpg(ImageFormat):
    def read(self):
        return cv2.imread(self.filename)

class Dcm(ImageFormat):
    def read(self):
        dcm = pydicom.read_file(self.filename)
        return dcm.pixel_array

class ImageReader:
    def __new__(cls, filename: str):
        fname, ext = filename.split(".")
        for format in ImageFormat.__subclasses__():
            if ext == format.__name__.lower():
                return format(filename)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    # A = ImageReader("C:/Users/kevin/Pictures/110641.jpg")
    from IPython import embed; embed()