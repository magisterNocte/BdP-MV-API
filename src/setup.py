from setuptools import find_packages, setup

setup(name="MV_Automatisierung",
      version="1.0",
      packages=find_packages(),
      install_requires=["openpyxl", "requests", "python-decouple"],
      extras_require={
          'opt1': ['autopep8'],
      }
      )
