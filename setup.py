from distutils.core import setup

setup(
    name='ktcal2',
    version='0.1.0',
    packages=['ktcal2', 'ktcal2.lib'],
    url='https://github.com/cr0hn/ktcal2',
    install_requires=["PyCrypto", "asyncssh-unofficial"],
    license='BSD',
    author='cr0hn',
    author_email='cr0hn<-at->cr0hn.com',
    description='SSH brute forcer tool and library, using AsyncIO of Python 3.4',
    scripts=["ktcal2/ktcal2.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
