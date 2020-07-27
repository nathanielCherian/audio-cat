import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_requirements():
    with open('requirements.txt') as requirements:
        req = requirements.read().splitlines()
    return req

setuptools.setup(
    name="audio-supervisor",
    version="0.0.1",
    author="Nathaniel Cherian",
    author_email="nathaniel@sylica.com",
    description="audio splitter and labeler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nathanielCherian/audio-supervisor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires= get_requirements(),

)