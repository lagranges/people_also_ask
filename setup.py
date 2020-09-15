import setuptools

version = {}

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="people_also_ask",
    version="0.0.2",
    author="LE Van Tuan",
    author_email="leavantuan2312@gmail.com",
    packages=setuptools.find_packages(),
    long_description=long_description,
    download_url="https://github.com/lagranges/people_also_ask/archive/0.0.1.tar.gz",
    install_requires=[
        "beautifulsoup4",
        "requests",
    ],
    python_requires=">=3.6"
)
