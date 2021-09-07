# Sevy's bastardization of https://github.com/python/cpython/blob/main/Lib/shutil.py

import os
from shutil import copy2, ignore_patterns
import fnmatch


def hardcopy_patterns(*patterns):
    def _hardcopy_patterns(path, names):
        matched_names = []
        for pattern in patterns:
            matched_names.extend(fnmatch.filter(names, pattern))
        return set(matched_names)
    return _hardcopy_patterns


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

    if hardcopy is not None:
        hardcopy_names = hardcopy(os.fspath(src), names)
    else:
        hardcopy_names = set()

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
                copytree_sym(srcname, dstname, symlinks=symlinks, hardcopy=hardcopy)
            else:
                # if srcname in hardcopy:
                if name in hardcopy_names:
                    copy2(srcname, dstname)
                else:
                    os.symlink(srcname, dstname)
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
    ),
    # hardcopy=('/home/moon/rmg/RMG-database/input/kinetics/families/Surface_Abstraction/rules.py')
    hardcopy=hardcopy_patterns(
        'rules[0-9][0-9][0-9][0-9].py',
        'reactions_[0-9][0-9][0-9][0-9].py',
        'surfaceThermoPt111_[0-9][0-9][0-9][0-9].py',
        # 'Surface_Abstraction.rules.py',
        # 'Surface_Abstraction.groups.py'
    )
)
