from setuptools import setup, find_packages

setup(
    name='topsis102203640',
    version='0.1.1',  # Minor version update for improvements
    description='A basic TOPSIS package for decision analysis.',
    author='stavya',
    author_email='sgoel2_be22@thapar.edu',
    url='https://github.com/stavyagoel/topsis',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pandas',
        'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
