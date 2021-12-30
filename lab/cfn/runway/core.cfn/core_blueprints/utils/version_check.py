"""Version check methods for blueprints.

Logic from http://stackoverflow.com/a/11887885
"""

from distutils.version import LooseVersion
import sys
import pkg_resources


def need(version, pkg='stacker'):
    """Verify Stacker is at a given version."""
    pkg_version = pkg_resources.get_distribution(pkg).version  # noqa pylint: disable=E1101
    if LooseVersion(pkg_version) < LooseVersion(version):
        print ''
        print 'ERROR!'
        print 'This blueprint requires %s >= %s' % (pkg, version)
        print 'Update your version of %s!' % pkg
        print ('(e.g. "pip install --user --upgrade %s" or "pip '
               'install --user --upgrade %s==%s" for alpha/beta '
               'releases)' % (pkg, pkg, version))
        print ''
        sys.exit()
