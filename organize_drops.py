''' Author: Jake Brinkmann, copyright 2016 '''
from glob import glob
from os import path, makedirs
from datetime import datetime, timedelta
import argparse
import shutil

import yaml


def get_file_stats(fname):
    # Get the filename/modified of a local file
    mtime = datetime.fromtimestamp(path.getmtime(fname))
    ctime = datetime.fromtimestamp(path.getctime(fname))
    dset = {'filename': fname,
            'modified': mtime,
            'created': ctime}
    return dset


def _dir(folder):
    # Return top-level items in a directory
    if path.isfile(folder):
        return [folder]
    else:
        return glob(path.join(folder, '*'))


def _walk(folder, depth=0, maxdepth=4):
    # Return list of only files within root directory
    files = _dir(folder)
    type_f = []
    for fn in files:
        if depth > maxdepth:
            return type_f
        if not path.isfile(fn):
            type_f += _walk(fn, depth+1, maxdepth)
        else:
            type_f.append(fn)
    return type_f


def get_most_recent(folder):
    # Returns the results of `get_file_stats` for the most recently modfied
    stats = []
    files = _walk(folder)
    if len(files):
        for fn in files:
            info = get_file_stats(fn)
            stats.append(info)
        maxtime = max([f['modified'] for f in stats])
        dset = filter(lambda x: x['modified'] == maxtime, stats)[0]
        dset.update({'filename': folder})
        return dset
    else:
        return get_file_stats(folder)


class Organize():
    def __init__(self, folder):
        # Find all files (modified dates, etc.)
        if not path.exists(folder):
            print('! Folder %s not found!' % folder)
            exit(1)
        self.folder = folder
        filenames = glob(path.join(folder, '*'))
        print('Found %d files.' % len(filenames))
        if len(filenames) < 1:
            print('! No files found!')
            exit(1)
        self.data = []
        for fn in filenames:
            dset = get_most_recent(fn)
            self.data.append(dset)

    def parse(self, threshold):
        # Determine new files destination
        cutoff = datetime.now() - timedelta(days=threshold)

        def parser(x):
            return x['modified'] < cutoff

        self.data = filter(parser, self.data)

    def move(self, root, sub, dry_run):
        # Move the files to the destination
        if dry_run:
            print(('*' * 10) + 'Nothing will be done' + '*' * 10)
        for dset in self.data:
            root_i = dset['modified'].strftime(root)
            sub_i = dset['modified'].strftime(sub)
            dest = path.join(self.folder, root_i, sub_i)
            if not path.exists(dest):
                print('-- Make %s --' % dest)
                if not dry_run:
                    makedirs(dest)
            print('Moving "%s" --> %s' %
                  (path.basename(dset['filename']), dest))
            if not dry_run:
                shutil.move(dset['filename'], dest)


def main(folder, days, nm_main, nm_sub, dry_run):
    search = Organize(folder)
    search.parse(days)
    search.move(nm_main, nm_sub, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', '-c', type=str, default='organizer.yml',
                        help='yaml config file [%(default)s]')
    parser.add_argument('--dry-run', '-d', action='store_true')
    args = parser.parse_args()
    with open(args.config) as fid:
        config = yaml.safe_load(fid)

    main(config['folder'], config['days'],
         config['fmt_root'], config['fmt_sub'], args.dry_run)
