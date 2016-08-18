# from distutils.core import setup, find_packages
from setuptools import setup, find_packages

setup(
    name='ktcal2',
    version='0.1.7',
    packages=find_packages(),
    url='https://github.com/cr0hn/ktcal2',
    install_requires=["asyncssh"],
    license='BSD',
    author='cr0hn',
    author_email='cr0hn<-at->cr0hn.com',
    description='SSH brute forcer tool and library, using AsyncIO of Python >= 3.4',
    entry_points={'console_scripts': [
        'kt-cal2 = ktcal2.kt_cal2:main',
    ]},
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
    ]
)
