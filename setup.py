from setuptools import setup, find_packages
# List of requirements
requirements = []  # This could be retrieved from requirements.txt
# Package (minimal) configuration
setup(
    name="src",
    version="1.0.0",
    description="Master's thesis",
    packages=find_packages(),  # __init__.py folders search
    install_requires=requirements
)
