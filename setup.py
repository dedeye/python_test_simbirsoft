from setuptools import find_packages
from setuptools import setup

setup(
    name="animalfilter",
    version="0.0.1",


    # maintainer="Pallets team",
    # maintainer_email="contact@palletsprojects.com",
    description="test assignment for simbirsoft",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "SQLAlchemy", "Pillow", "requests"],
    extras_require={"test": ["pytest", "coverage"]},
)