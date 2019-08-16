# coding=utf-8

from setuptools import setup, find_packages

import os

def find_requires():
    fp = open("requirements.txt", "r")
    for line in fp.readlines():
        if line.startswith("#") or line.startswith("--"):
            continue
        else:
            yield line.strip()

setup(
    name="captcha",
    version="0.0.1",
    description="a simple implement of image and audio (wait to implement) captcha",
    author="linghaihui",
    author_email="haihuiling2014@gmail.com",
    url="https://github.com/linghaihui/captcha",
    packages=["captcha"],
    install_requires=list(find_requires()),
    include_package_data=True,
)