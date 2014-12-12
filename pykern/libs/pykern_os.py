from pykern.filesystem import FileSystem, calculate_absolute


class stat_result(object):
    def __init__(self, st_mode, st_size):
        self.st_mode = st_mode
        self.st_size = st_size

    def __repr__(self):
        return '<stat_result: st_size=%d>' % self.st_size


def mkdir(dirname):
    import stat
    fs = FileSystem()
    if dirname in fs.metadata or dirname in ('.', '..'):
        raise IOError('File exists')
    if '/' in dirname:
        raise ValueError('"/" is not permitted in directory name')
    fs.add_item(dirname, stat.S_IFDIR)


def chdir(path):
    import os
    fs = FileSystem()
    absolute_path = calculate_absolute(fs.current_dir, '%s' % path)
    if not os.path.isdir(absolute_path):
        raise OSError('Not a directory: "%s"' % path)
    fs.current_dir = absolute_path


def listdir(path):
    fs = FileSystem()
    absolute_target_path = calculate_absolute(fs.current_dir, '%s/' % path)
    return [path[len(absolute_target_path):]
            for path in FileSystem().metadata.keys() if path.startswith(absolute_target_path)]


def stat(path):
    fs = FileSystem()
    path = calculate_absolute(fs.current_dir, path)
    try:
        file_ = fs.metadata[path]
    except KeyError:
        raise OSError('No such file "%s"' % path)

    return stat_result(file_['mode'], file_['size'])
