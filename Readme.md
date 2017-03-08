# Review scripts for CISC 3620

This repository contains review scripts for the topics covered in CISC 3620. Each script covers one topic and generates questions on the fly. The midterm and final will be generated from these reviews.

## Installing Python

The scripts are in Python 3. You can download Python [here](https://www.python.org/downloads/). Choose the appropriate link for your operating system. Make sure the version you get is above 3. Run the installer.

## Installing dependencies

### Image, numpy

The scripts include some Python packages. You can install them using pip, which is included in the Python installation if it is above 3.4. To upgrade pip, run from the command line:

```
pip install -U pip setuptools	# Linux or OS X
python -m pip install -U pip setuptools	# Windows
```

Then, use pip to install:

```
pip install numpy
pip install Pillow
```

### R, ggplot

[download page](http://lib.stat.cmu.edu/R/CRAN/), choose the appropriate link for your operating system. Run the installer.

Once R has been installed, type `R` at the command line. This should take you into an interactive R session. At the prompt, type `install.packages("ggplot2")` and press Enter. Choose from the list of mirrors the closest one to where you are and type its number at the prompt. Once the package has been downloaded, type `q()` to quit.

# Ask for help
Open an issue on this repository if any of this doesn't work for you. Please include details about your platform, what you've tried, and what error you got.
