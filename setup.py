# from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(
    name='ktcal2',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/cr0hn/ktcal2',
    # install_requires=["PyCrypto", "asyncssh-unofficial"],
    license='BSD',
    author='cr0hn',
    author_email='cr0hn<-at->cr0hn.com',
    description='SSH brute forcer tool and library, using AsyncIO of Python 3.4',
    entry_points={'console_scripts': [
        'kt-cal2 = ktcal2.bin.kt_cal2:main',
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
