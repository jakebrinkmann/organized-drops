''' Author: Jake Brinkmann, copyright 2016 '''
from glob import glob
from os import path, makedirs
from datetime import datetime, timedelta
import argparse
import shutil

import yaml

class Organize():
    def __init__(self, folder):
        # Find all files (modified dates, etc.)
        self.folder = folder
        filenames = glob(path.join(folder, '*'))
        self.data = []
        for fn in filenames:
            mtime = datetime.fromtimestamp(path.getmtime(fn))
            ctime = datetime.fromtimestamp(path.getctime(fn))
            dset = {'filename': fn,
                    'modified': mtime,
                    'created': ctime}
            self.data.append(dset)

    def parse(self, threshold):
        # Determine new files destination
        cutoff = datetime.now() - timedelta(days=threshold)
        parser = lambda x: x['modified'] < cutoff
        self.data = filter(parser, self.data)

    def move(self, root, sub, dry_run):
        # Move the files to the destination
        if dry_run:
            print(('*' * 10) + 'Nothing will be done' + '*' * 10)
        for dset in self.data:
            root_i = dset['modified'].strftime(root)
            sub_i = dset['modified'].strftime(sub)
            dest = path.join(self.folder, root_i, sub_i)
            if not path.exists(dest) and not dry_run:
                makedirs(dest)
            print('Moving "%s" to %s' %
                  (path.basename(dset['filename']), dest))
            if not dry_run:
                shutil.move(dset['filename'], dest)


def main(folder, days, nm_main, nm_sub, dry_run):
    search = Organize(folder)
    search.parse(days)
    search.move(nm_main, nm_sub, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', '-c', type=str, nargs=1,
                        default='organizer.yml',
                        help='yaml config file [%(default)s]')
    parser.add_argument('--dry-run', '-d', action='store_true')
    args = parser.parse_args()
    with open(args.config) as fid:
        config = yaml.safe_load(fid)

    main(config['folder'], config['days'],
         config['fmt_root'], config['fmt_sub'], args.dry_run)
