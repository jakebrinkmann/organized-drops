''' Author: Jake Brinkmann, copyright 2016 '''
from glob import glob
from os import path, makedirs
from datetime import datetime, timedelta
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

    def move(self, root, sub):
        # Move the files to the destination
        for dset in self.data:
            root_i = dset['modified'].strftime(root)
            sub_i = dset['modified'].strftime(sub)
            dest = path.join(self.folder, root_i, sub_i)
            if not path.exists(dest):
                makedirs(dest)
            print('Moving "%s" to %s' % (path.basename(dset['filename']), dest))
            shutil.move(dset['filename'], dest)


def main(folder, days, nm_main, nm_sub):
    search = Organize(folder)
    search.parse(days)
    search.move(nm_main, nm_sub)


if __name__ == "__main__":
    with open('organizer.yml') as fid:
        config = yaml.safe_load(fid)

    main(config['folder'], config['days'],
         config['fmt_root'], config['fmt_sub'])
