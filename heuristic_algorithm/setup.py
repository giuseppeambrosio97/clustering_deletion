from setuptools import setup, find_packages
import os

# Read requirements
requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
with open(requirements_file, "r") as f:
    requirements = f.read().splitlines()

pkg_name = "heuristic_algorithm"

# Package configuration
setup(name=pkg_name,
      version="0.0.0",
      description="Clustering Deletion Heuristic Algorithm",
      packages=find_packages(), # __init__.py folders search
      install_requires=requirements)
