from setuptools import find_packages
from setuptools import setup

setup(
    name="animalfilter",
    version="0.0.1",

    description="test task for simbirsoft",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["Flask==1.1.2", "Flask-SQLAlchemy==2.4.3", "Pillow==7.1.2", "requests==2.31.0"],
)