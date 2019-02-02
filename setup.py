import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='amfibious',
    version='0.1.0',
    url='https://github.com/mayurbhangale/amfibious',
    license='MIT',
    author='Mayur Bhangale',
    author_email='mayurbhangale96@gmail.com',
    packages=setuptools.find_packages(),
    description='put something good here',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],
)
