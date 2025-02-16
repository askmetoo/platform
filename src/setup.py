from setuptools import setup
from os.path import join, dirname

version = open(join(dirname(__file__), 'version')).read().strip()

setup(
    name='syncloud-platform',
    version=version,
    packages=['syncloud_platform',
              'syncloud_platform.insider',
              'syncloud_platform.auth',
              'syncloud_platform.gaplib',
              'syncloud_platform.config',
              'syncloud_platform.control',
              'syncloud_platform.disks'],
    namespace_packages=['syncloud_platform'],
    description='Syncloud platform',
    long_description='Syncloud platform',
    license='GPLv3',
    author='Syncloud',
    author_email='syncloud@googlegroups.com',
    url='https://github.com/syncloud/platform')
