"""Installer for serverdensity-hb-plugin
"""

import os
cwd = os.path.dirname(__file__)
__version__ = open(os.path.join(cwd, 'serverdensity_hb_plugin', 'version.txt'), 'r').read().strip()

try:
        from setuptools import setup, find_packages
except ImportError:
        from ez_setup import use_setuptools
        use_setuptools()
        from setuptools import setup, find_packages
setup(
    name='serverdensity_hb_plugin',
    description='ServerDensity.com API plugin for hippybot',
    version=__version__,
    author='Wes Mason',
    author_email='wes@boxedice.com',
    url='http://github.com/boxedice/serverdensity-hb-plugin',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=open('requirements.txt').readlines(),
    package_data={'serverdensity_hb_plugin': ['version.txt']},
    include_package_data=True,
    license='BSD'
)
