from PySide6.QtGui import QPainter, QPixmap, QPainterPath
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget
from tinytag import TinyTag
from io import BytesIO
from PIL import Image
import PIL
import pickle
import os

class SongIcon(QWidget):
    def __init__(self, parent=None, song_data = None):
        super().__init__(parent)
        self.song_data = song_data
        self.setFixedSize(150, 150)

    def paintEvent(self, event):  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        img = self.get_img_data(self.song_data[2])
        if not img:
            QSvgRenderer("Assets/file-music.svg").render(painter, self.rect())
        else:
            img_map = QPixmap()
            img_map.loadFromData(img)

            # Add a rounded corner
            path = QPainterPath()
            path.addRoundedRect(self.rect(), 10, 10)
            painter.setClipPath(path)

            painter.drawPixmap(self.rect(), img_map)

    def get_img_data(self, file_path: str, *, resolution: tuple = (150, 150)) -> bytes | bool:
        cache_dir = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache') + '/SoundDrive/covers/')
        cache_path = cache_dir + os.path.basename(file_path) + str(resolution) + '.cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Check if the image data is cached and return
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                img_data = pickle.load(f)
            return img_data

        # Load the image
        tag = TinyTag.get(file_path, image=True)
        img_data = tag.get_image()

        # Resize the image
        try:
            image = Image.open(BytesIO(img_data))
            image = image.resize(resolution, Image.LANCZOS)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_data = img_byte_arr.getvalue()
        except PIL.UnidentifiedImageError:
            return False

        # Cache the image data
        with open(cache_path, 'wb') as f:
            pickle.dump(img_data, f)
        return img_data
