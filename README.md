# Organized Drops

I use my "drop-box" a bit too literally, so I thought I could find a way to
keep it more manageable.

## Description

A python script to find files in a folder older than a certain date, and
subsequently organize these files into a new folder hierarchy.

## Install

To install using pip:

    pip install -r requirements.txt

## Usage

When used from the command-line:

    cp organizer.yml.sample organizer.yml
    edit organizer.yml
    python oranize_drops.py -c organizer.yml

### results

The results will be formatted in a tree:

    2016
    |-- Apr
    \-- Oct
