import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
INSTALL_REQUIREMENTS = ["Pillow"]
TEST_REQUIREMENTS = ["mock"]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pydenticon',
    version='0.3.1',
    packages=['pydenticon'],
    include_package_data=True,
    license='BSD',  # example license
    description='Library for generating identicons. Port of Sigil (https://github.com/cupcake/sigil) with enhancements.',
    long_description=README,
    url='https://github.com/azaghal/pydenticon',
    author='Branko Majic',
    author_email='branko@majic.rs',
    install_requires=INSTALL_REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite="tests",
    classifiers=[
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries',
    ],
)
