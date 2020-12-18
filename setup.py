import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlozaic",
    version="0.1.0",
    author="Kavi Gupta",
    author_email="mlozaic@kavigupta.org",
    description="A simple programming language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/mlozaic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=[
        "numpy==1.19.4",
        "attrs==20.3.0"
    ]
)
