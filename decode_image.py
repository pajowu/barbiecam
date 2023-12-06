import cv2
import numpy as np
import argparse


def decode_image(data: bytes, n_cols: int, n_black_lines: int, n_visible_lines: int):
    imsize = n_cols * n_visible_lines
    offset = n_cols * n_black_lines
    input_img = np.frombuffer(data[offset:], np.dtype("u1"), imsize).reshape(
        (n_visible_lines * 2, n_cols // 2)
    )

    bayer_img = np.zeros((n_visible_lines, n_cols), dtype="u1")
    bayer_img[::2, ::2] = input_img[1::4, :]
    bayer_img[::2, 1::2] = input_img[::4, :]
    bayer_img[1::2, ::2] = input_img[3::4, :]
    bayer_img[1::2, 1::2] = input_img[2::4, :]

    output_img = cv2.cvtColor(bayer_img, cv2.COLOR_BAYER_GRBG2BGR)
    return output_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    with open(args.input_file, "rb") as f:
        data = f.read()

    output_image = decode_image(data, n_cols=164, n_black_lines=2, n_visible_lines=124)
    cv2.imwrite(args.output_file, output_image)
