from skimage.feature import hog
from skimage.transform import resize
from io import BytesIO
from PIL import Image
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def preprocessing_img(row):
    img=np.array(Image.open(BytesIO(row['data'])).convert('L'))
    resized_img = resize(img, (128, 128), anti_aliasing=True)
    features = hog(
        resized_img,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm='L2-Hys',
        visualize=False
    )
    return features
