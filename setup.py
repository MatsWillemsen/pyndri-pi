from setuptools import setup, find_packages

setup(
    name='pyndri_pi',
    version='0.0.1',
    description='Native python indri-package',
    long_description='Native python indri-package',
    url='https://github.com/MatsWillemsen/pyndri-pi',
    author='Mats Willemsen',
    author_email='mats.willemsen@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT Licens',
        'rogramming Language :: Python :: 3.5',
    ],
    packages=find_packages(exclude=['contrib', 'doc', 'tests'])

)