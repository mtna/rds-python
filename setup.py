import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtna-rds",
    version="0.2.13",
    author="Metadata Technology North America Inc.",
    author_email="mtna@mtna.us",
    description="A library to query the Rich Data Services API framework developed by MTNA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtna/rds-python/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Database :: Database Engines/Servers",
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4'
)
