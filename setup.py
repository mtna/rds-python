import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rds-library",
    version="1.0.0",
    author="Metadata Technology North America Inc.",
    author_email="mtna@mtna.us",
    description="A library to query the Rich Data Services API framework developed by MTNA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtna/rds-python/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2, 3",
        "License :: OSI Approved :: Apache-2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='==2.7, >=3.6'
)
