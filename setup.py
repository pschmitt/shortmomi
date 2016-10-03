from distutils.core import setup

setup(
    name='shortmomi',
    version='1.6.1',
    description='Bundle of useful functions and shortcuts for pyVmomi',
    author='Philipp Schmitt',
    author_email='philipp@schmitt.co',
    url='https://github.com/pschmitt/shortmomi',
    packages=['shortmomi'],
    install_requires=['pyvmomi']
)
