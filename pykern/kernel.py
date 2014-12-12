import sys

from filesystem import FileSystem
from pykern.libs import patch_libs
from pykern.shell import Shell


class Kernel(object):
    def __init__(self, fs_file_name):
        self.filesystem = FileSystem(fs_file_name)
        self.substitue_libs()

    def boot(self):
        Shell(self).run()

    def substitue_libs(self):
        patch_libs()
        self.filesystem.patch_all()

    def run_file(self, filename, args):
        with open(filename) as f:
            sys.argv = args
            result = self.run_code(f.read())
            sys.argv = []
            return result

    def run_code(self, code):
        try:
            exec compile(code, '<string>', 'exec') in {'__name__': '__main__'}
        except:
            return False
        else:
            return True
