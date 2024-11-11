# Ancestry PDF to JPEG Converter
Turn a multi-page Ancestry family tree PDF into a single JPEG for easier viewing and printing.

This is a small code package that can be used to take a family tree PDF that Ancestry provides and convert it into a single image. One might wish to do this for an easier time printing a whole family tree, or simply having a single, high resolution photo of a family tree that doesn't require paying for one using a third-party site.

This code has been tested using Python 3.8, but will likely work on more versions.

## Usage
```
usage: jpg_join [-h] -f FILE [-s SAVE_FILE] [-r ROWS] [-c COLS] [--h-trim H_TRIM] [--v-trim V_TRIM] [--save-each-jpeg] [--tb-ratio TB_RATIO]

Combine PDF pages into a single JPEG. 
 
NOTE: it is highly recommended to print your tree from Ancestry with NO BORDERS

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  filepath of PDF to be joined
  -s SAVE_FILE, --save-file SAVE_FILE
                        filename of destination JPEG, default to input filename
  -r ROWS, --rows ROWS  number of rows in the supplied grid
  -c COLS, --cols COLS  number of columns in the supplied grid
  --h-trim H_TRIM       number of pixels to trim from the left and right of each page
  --v-trim V_TRIM       number of pixels to trim from the top and bottom of each page
  --save-each-jpeg      Set this flag if individual JPEGs are wanted, default to delete temp files
  --tb-ratio TB_RATIO   The ratio between the border side of the top border and bottom border. If you find that the lower border is cut off too much and
                        the upper not enough (or vice versa), adjust this value
```

## Example

### Create a virtual environment
```bash
python -m venv .venv
source ./venv/bin/activate
```

### Install requirements
```bash
pip install "."
```

### Run the program
```bash
python -m ancestry_pdf_to_jpeg.main -f ancestry_pdf.pdf
```

Minor adjustments can be made using the arguments listed under Usage.

## Tips for getting the PDF

1. Use the "tree view" tool in Ancestry to look at the tree you want to print.
2. Manually expand all of the family members you wish to be a part of your tree (at this time, this doesn't appear to be possible to automate)
3. Using the toolbar, look under "More" (the three dots), and select "Print"
4. In the print window, change the destination to "Save as PDF"
5. Under Margins, select "None". This will make combining the photos easier later.
6. Save the PDF to the directory where you will be running the program to join the PDF pages into a singular image.