import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    """Optionally print a message about running slips-setup manually."""
    def run(self):
        install.run(self)
        print("\n[INFO] Installation complete.\nTo install system-level dependencies, run:\n  slips-setup\n")


setup(
    name="slips-sdk",
    version="0.1.0",
    author="Jenil Vekariya",
    author_email="vekariyajenil888@gmail.com",
    description="SDK for interacting with slips IDS components",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["slips", "slips.*"]),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.10',
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'slips-setup=slips.slips_setup:main',
        ],
    },
)
