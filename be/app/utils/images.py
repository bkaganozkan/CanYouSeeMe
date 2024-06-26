import random
import numpy as np
from PIL import Image
import os

height = 465
width = 465


db_path = os.path.join("static", "images")
image_dir = os.path.join("app", db_path)

if not os.path.exists(image_dir):
    os.makedirs(image_dir)


def generate_noisy_image(filename):
    chessboard_size = 6
    square_size = height // chessboard_size

    image = Image.new("RGB", (width, height))

    # Fill the image with 6x6 squares of random colors
    for row in range(chessboard_size):
        for col in range(chessboard_size):
            color = tuple(
                np.random.randint(0, 256, size=3).tolist()
            )  
            for i in range(square_size):
                for j in range(square_size):
                    image.putpixel(
                        (col * square_size + i, row * square_size + j), color
                    )

    image_path = os.path.join(image_dir, filename)
    image.save(image_path, format="JPEG")

    return os.path.join(db_path, filename)
