# -*- coding:utf-8 -*-
import pathlib
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='joblet.common',
    version='2.0.0',
    description='A simple app boilerplate.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Junzki/joblet.common',
    author='Andrew Junzki',
    author_email='andrew@junzki.me',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=find_packages(where=str(here)),
    python_requires='>=3.6, <4',
    install_requires=(here / 'requirements.txt').read_text().split('\n')
)
