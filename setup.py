from setuptools import find_packages, setup


setup(
    name="shortmomi",
    version="1.9.1",
    license="GPL3",
    description="Bundle of useful functions and shortcuts for pyVmomi",
    author="Philipp Schmitt",
    author_email="philipp@schmitt.co",
    url="https://github.com/pschmitt/shortmomi",
    packages=find_packages(),
    install_requires=["pyvmomi"],
)
