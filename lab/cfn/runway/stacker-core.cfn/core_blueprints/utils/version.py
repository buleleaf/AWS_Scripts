"""Retrieve platform version from top of repository."""

from os.path import basename, dirname, realpath
import sys

FILE_PATH = dirname(realpath(__file__))
PARENT_PATH = dirname(FILE_PATH)


def version():
    """Call version function from top of repo."""
    current_dir = basename(FILE_PATH)  # e.g. utils
    rel_dir = "%s.%s" % (basename(PARENT_PATH), current_dir)  # foo.utils
    if __package__ in [None, current_dir, rel_dir]:
        sys.path.append(
            dirname(dirname(dirname(dirname(FILE_PATH))))
        )
    import platform_version  # pylint: disable=import-error
    return platform_version.version()
