#!/usr/bin/env python

"""
File: main.py
Author: John Alling
Date: 27 December 2023
Description: A quick utility for taking PDF trees from Ancestry.com and combining them into a single JPEG
"""

# imports
import argparse
import os
import sys
import tempfile
from contextlib import contextmanager
from pdf2image import convert_from_path
from PIL import Image

@contextmanager
def managed_image(path):
    "Handle a temporary image."
    img = Image.open(path)
    try:
        yield img
    finally:
        img.close()

def main():
    "Primary logic for converting/joining the image."
    # argument parsing
    parser = argparse.ArgumentParser(
        prog="ancestry_pdf_to_jpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Combine PDF pages into a single JPEG. \n \nNOTE: it is highly recommended to print your tree from Ancestry with NO BORDERS",
    )

    parser.add_argument("-f", "--file", required=True, help="filepath of PDF to be joined")
    parser.add_argument(
        "-s", "--save-file", help="filename of destination JPEG, default to input filename"
    )
    parser.add_argument(
        "-r", "--rows", type=int, default=4, help="number of rows in the supplied grid"
    )
    parser.add_argument(
        "-c", "--cols", type=int, default=5, help="number of columns in the supplied grid"
    )
    parser.add_argument(
        "--h-trim",
        type=int,
        default=2,
        help="number of pixels to trim from the left and right of each page",
    )
    parser.add_argument(
        "--v-trim",
        type=int,
        default=110,
        help="number of pixels to trim from the top and bottom of each page",
    )
    parser.add_argument(
        "--save-each-jpeg",
        action="store_true",
        help="Set this flag if individual JPEGs are wanted, default to delete temp files",
    )
    parser.add_argument(
        "--tb-ratio",
        type=float,
        default=2.1,
        help="The ratio between the size of the top and bottom borders. \
                                                                If you find that the lower border is cut off too much and the upper not enough (or vice versa), adjust this value",
    )

    args = parser.parse_args()
    print(args)

    # set constants from arguments
    ROWS = args.rows
    COLS = args.cols

    # convert PDF to individual JPEGs
    print("Converting from PDF to JPEG...")
    try:
        pdf_pages = convert_from_path(args.file, dpi=200)
    except Exception as e:
        print(f"Error converting PDF: {e}")
        sys.exit(1)
    if len(pdf_pages) != (ROWS * COLS):
        raise ValueError(
            f'The number of images converted ({len(pdf_pages)}) does not match the requested number ({ROWS*COLS}). \n \
                Please adjust the number of rows and columns using the "--rows" and "--cols" arguments'
        )
    print("PDF conversion complete!")

    with tempfile.TemporaryDirectory() as temp_dir:      
        # temporarily store individual JPEGs
        imgs = []
        for count, page in enumerate(pdf_pages):
            temp_path = os.path.join(temp_dir, f"{count+1}.jpg")
            page.save(temp_path, "JPEG")
            imgs.append(temp_path)

        with managed_image(imgs[0]) as img1:
            img_size = img1.size
            print(f"old size: {img_size}")

            # set how much to trim from images
            TOP_BOTTOM_RATIO = args.tb_ratio

            LEFT = args.h_trim
            UPPER = args.v_trim
            LOWER = img_size[0] - args.h_trim
            RIGHT = int(img_size[1] - TOP_BOTTOM_RATIO * (args.v_trim))

            # create empty image to hold final image data
            img1 = img1.crop((LEFT, UPPER, LOWER, RIGHT))
            img_size = img1.size  # get the new size
            print(f"new size: {img_size}")
            img1.close()

        final_image = Image.new(
            "RGB", (COLS * img_size[0], ROWS * img_size[1]), (255, 255, 255)
        )
        print(f"final image size: {final_image.size}")

        # paste individual JPEGs to final image
        print("Stitching images together...")
        for ii in range(ROWS):
            for jj in range(COLS):
                img_num = (
                    jj + (ii * COLS)
                )  # get the image number to be read from this folder (non-zero index)
                sys.stdout.write(f"Progress: {img_num}/{len(imgs)} \r")
                with managed_image(imgs[img_num]) as curr_image:
                    curr_image = curr_image.crop((LEFT, UPPER, LOWER, RIGHT))
                    final_image.paste(curr_image, (jj * img_size[0], ii * img_size[1]))
                sys.stdout.flush()

        # save the finished image
        if args.save_file:
            save_name = args.save_file
        else:
            save_name = args.file.split(".")[0] + ".jpg"
        final_image.save(save_name)
        final_image.close()
        print("Image completed!")

if __name__ == "__main__":
    main()
    