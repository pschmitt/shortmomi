from distutils.core import setup

setup(
    name='pyvmomi-lib',
    version='1.4',
    description='Bundle of useful functions for pyVmomi',
    author='Philipp Schmitt',
    author_email='philipp.schmitt@post.lu',
    url='https://git.3s.dt.ept.lu/ict-infra/pyvmomi-lib',
    packages=['pyvmomilib'],
    install_requires=['pyvmomi']
)
