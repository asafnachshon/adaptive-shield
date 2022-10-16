import os

from setuptools import Command, find_packages, setup
from setuptools.command.install import install


class _InstallCommand(install):
    def run(self):
        install.run(self)


class _TestCommand(Command):
    root_dir = os.path.split(os.path.abspath(__file__))[0]
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system(
            f"coverage erase && "
            f"coverage run --branch --source={self.root_dir}/adaptive_shield -m unittest discover test -s "
            f"{self.root_dir}/tests/* -p *_test.py && "
            f"coverage xml -i"
        )


setup(
    name="adaptive_shield",
    version="1.0.0",
    url="https://github.com/asafnachshon/adaptive-shield",
    packages=find_packages(exclude=[]),
    entry_points={
        "console_scripts": [
            "start_adaptive_shield = adaptive_shield.service:main",
        ]
    },
    include_package_data=True,
    cmdclass={
        "install": _InstallCommand,
        "test": _TestCommand,
    },
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
)
