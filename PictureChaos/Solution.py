import numpy as np
import sys
from PIL import Image


def dechaos(image, FLAG):
    pil_image = Image.fromarray(image).transpose(FLAG)
    np_image = np.array(pil_image)
    for i in range(np_image.shape[0]):
        for j in range(np_image.shape[1]):
            image[i, j] = np_image[i, j]


def solve(image):
    SIDE_SIZE = image.shape[1]//2
    first_quarter = image[:SIDE_SIZE, :SIDE_SIZE]
    second_quarter = image[:SIDE_SIZE, SIDE_SIZE:SIDE_SIZE*2]
    third_quarter = image[SIDE_SIZE:SIDE_SIZE*2, :SIDE_SIZE]
    fourth_quarter = image[SIDE_SIZE:SIDE_SIZE*2, SIDE_SIZE:SIDE_SIZE*2]
    if SIDE_SIZE > 2:
        solve(first_quarter)
        solve(second_quarter)
        solve(third_quarter)
        solve(fourth_quarter)
    dechaos(second_quarter, FLAG=Image.FLIP_LEFT_RIGHT)
    dechaos(third_quarter, FLAG=Image.ROTATE_90)
    dechaos(fourth_quarter, FLAG=Image.ROTATE_270)


def main(image_name, output_name):
    pil_image = Image.open(image_name)
    np_image = np.array(pil_image)
    if tuple(map(lambda x: x % 4, np_image.shape))[:2] != (0, 0):
        print(f"Shape {np_image.shape} is incorrect!")
        return

    solve(np_image)
    Image.fromarray(np_image).save(output_name)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Give me an image!")
    else:
        main(sys.argv[1], sys.argv[2])
