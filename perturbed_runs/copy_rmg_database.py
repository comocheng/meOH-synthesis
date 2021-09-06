# Sevy's bastardization of https://github.com/python/cpython/blob/main/Lib/shutil.py

import os
from shutil import copy2, copystat, ignore_patterns
import fnmatch


def ignore_patterns(*patterns):
    """Function that can be used as copytree() ignore parameter.
    Patterns is a sequence of glob-style patterns
    that are used to exclude files"""
    def _ignore_patterns(path, names):
        ignored_names = []
        for pattern in patterns:
            ignored_names.extend(fnmatch.filter(names, pattern))
        return set(ignored_names)
    return _ignore_patterns


# start by copying a directory but ignoring the .git
def copytree_sym(src, dst, ignore=None, hardcopy=None, symlinks=False):
    """
    Copies a tree mostly symbolically. It will make a physical copy of the
    files specified, and not copy any of the files on the ignore list.
    """
    names = os.listdir(src)
    os.makedirs(dst)

    if ignore is not None:
        ignored_names = ignore(os.fspath(src), names)
    else:
        ignored_names = set()

    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree_sym(srcname, dstname, symlinks)
            else:
                # TODO - check if this should be hardcopied
                os.symlink(srcname, dstname)
                # copy2(srcname, dstname)  instead of actually copying
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Exception as err:
            errors.extend(err.args[0])
    # try:
    #     copystat(src, dst)
    # except OSError as why:
    #     # can't copy file access times on Windows
    #     if why.winerror is None:
    #         errors.extend((src, dst, str(why)))
    # if errors:
    #     raise OSError(errors)


database_src = "/home/moon/rmg/RMG-database/"
database_dest = "/home/moon/rmg/db_copy/db0/"
if not os.path.exists(database_src):
    raise OSError(f'Could not find source database {database_src}')
if os.path.exists(database_dest):
    raise OSError(f'Destination already exists: {database_dest}')

copytree_sym(
    database_src,
    database_dest,
    symlinks=True,
    ignore=ignore_patterns(
        '.conda',
        '.git',
        '.github',
        '.gitignore',
        '.travis.yml',
        '.vscode',
    )
)
