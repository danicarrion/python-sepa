# -*- coding: utf-8 -*-
from setuptools import setup

setup(name="python-sepa",
      author="Daniel Carrión",
      author_email="dani@computados.com",
      description="Single Euro Payments Area file generation for Python",
      version="0.0.1.dev7",
      license="MIT",
      include_package_data=True,
      url="https://github.com/danicarrion/python-sepa",
      install_requires=['Jinja2'],
      packages=["sepa"]
)
