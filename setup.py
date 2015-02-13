#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# try:
from setuptools import setup
#     setup  # workaround for pyflakes issue #13
# except ImportError:
#     from distutils.core import setup

# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
# try:
#     import multiprocessing
#     multiprocessing
# except ImportError:
#     pass

setup(
    name='AddVCalToGoogle',
    version='0.0.0',
    author='Alexis Lee',
    author_email='avtg@lxsli.co.uk',
    packages=[],
    scripts=['bin/add-vcal'],
    url='http://github.com/lxsli/add-vcal-to-google',
    license='LICENSE',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
    ],
    description='Commandline tool to parse a VCAL event and add it to your'
                ' Google Calendar',
    install_requires=open('requirements.txt').readlines(),
)
