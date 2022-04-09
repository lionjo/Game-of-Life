from setuptools import find_namespace_packages, find_packages, setup

setup(
    name="GameOfLife",
    version="0.1",
    description="A codeframwork play around with Convey's 'Game of Life'",
    # url="https://gitlab.mpcdf.mpg.de/jtl/equi-surf",
    author="Jorrit Lion",
    author_email="jorrit.lion@gmail.com",
    license="MIT",
    packages=find_packages() + find_namespace_packages(),
    install_requires=["numpy", "matplotlib"],
    scripts=["scripts/GameOfLife.py"],
    python_requires=">=3.6.*",
    zip_safe=False,
)
