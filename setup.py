import codecs
import os.path
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


# Read the version number from a source file.
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='euvat-json-api',
      version=find_version('euvat-json-api'),
      description='JSON API server for EU VAT number validation',
      author='Nephics AB',
      author_email='euvat@nephics.com',
      license="Apache v2.0 (see LICENSE file)",
      url='https://github.com/nephics/euvat-json-api',
      scripts=['euvat-json-api'],
      install_requires=['tornado>=3.1.1'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Office/Business :: Financial',
          'Topic :: Internet :: Proxy Servers'
      ])
