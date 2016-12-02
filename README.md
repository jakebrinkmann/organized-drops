# Organized Drops

I use my "drop-box" a bit too literally, so I thought I could find a way to
keep it more manageable.

## Description

A python script to find files in a folder older than a certain date, and
subsequently organize these files into a new folder hierarchy.

## Install

To use this script, just download the _.py_ file and run with python. To clone
the entire repository:

    git clone https://github.com/jakebrinkmann/organized-drops.git
    cd organized-drops

### dependencies

To install the required package dependencies using pip:

    pip install -r requirements.txt

## Usage

Since the script should be run with some frequency, it can only be run using a
configuration file ([sample](./organizer.yml.sample)):

    cp organizer.yml.sample organizer.yml
    edit organizer.yml

When used from the command-line:

    python oranize_drops.py -c organizer.yml

There is also a `--dry-run` argument to prevent any actual file system
operations:

    python organize_drops.py -d -c organizer.yml

### results

The results will be formatted in a tree:

    Dropbox/
    ├── 2015
    │   └── Feb
    └── 2016
        ├── Apr
        └── Oct
