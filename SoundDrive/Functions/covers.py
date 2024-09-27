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
    :return: Either the cover or False
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

def get_playlist_icon(playlist_data: list[str], *, resolution: tuple = (200, 200), db_access: object) -> bytes:
    """
    Returns the icon of a playlist
    :param playlist_data: The data of the playlist
    :param resolution: The resolution of the cover
    :param db_access: The access to the db
    :return: Either the cover or False
    """
    displayed_song_ids = playlist_data[3].split(",")[:4]
    # Get cover for each song
    image_data = []
    for song_id in displayed_song_ids:
        song_data = db_access.songs.query_id(song_id)
        image_data.append(get_song_cover(song_data[2], resolution = tuple(int(res / 2) for res in resolution)))

    # Concat images
    image = Image.new('RGB', (resolution[0], resolution[1]))
    if len(image_data) >= 1:
        im1 = Image.open(BytesIO(image_data[0]))
        image.paste(im1, (0, 0))
    if len(image_data) >= 2:
        im2 = Image.open(BytesIO(image_data[1]))
        image.paste(im2, (int(resolution[0] / 2), 0))
    if len(image_data) >= 3:
        im3 = Image.open(BytesIO(image_data[2]))
        image.paste(im3, (0, int(resolution[1] / 2)))
    if len(image_data) >= 4:
        im4 = Image.open(BytesIO(image_data[3]))
        image.paste(im4, (int(resolution[0] / 2), int(resolution[1] / 2)))

    # Convert img to bytes and return
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_data = img_byte_arr.getvalue()
    return img_data
