from tinytag import TinyTag
from io import BytesIO
from PIL import Image
import pickle
import PIL
import os

def get_song_cover(file_path: str, *, resolution: tuple = (150, 150)) -> bytes | bool:
    """
    Gets the cover of a song
    :param file_path: Path to the song
    :param resolution: The resolution the cover should have
    :return: Either the cover or a False
    """
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
