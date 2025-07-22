import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstallCommand(install):
    """
    Custom installation to copy essential config directories
    to /etc/slips-sdk after package installation.
    """

    def run(self):
        # Run default installation
        install.run(self)

        # Define source and target paths
        project_root = os.path.abspath(os.path.dirname(__file__))
        source_dirs = [
            os.path.join(project_root, "slips", "StratosphereLinuxIPS", "config"),
            os.path.join(project_root, "slips", "StratosphereLinuxIPS", "dataset"),
            os.path.join(project_root, "slips", "StratosphereLinuxIPS", "databases"),
        ]
        target_root = "/etc/slips-sdk"

        print("\n[INFO] Copying configuration files to:", target_root)

        try:
            # Create target root if not exists
            os.makedirs(target_root, exist_ok=True)

            # Copy directories recursively
            for src in source_dirs:
                if os.path.exists(src):
                    dst = os.path.join(target_root, os.path.basename(src))
                    print(f"[INFO] Copying {src} → {dst}")
                    if os.path.exists(dst):
                        shutil.rmtree(dst)  # Remove existing directory
                    shutil.copytree(src, dst)
                else:
                    print(f"[WARNING] Directory not found: {src}")

            print("[INFO] All configuration directories copied successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to copy configuration directories: {e}")


setup(
    name="slips-sdk",
    version="0.1.2",
    author="Jenil Vekariya",
    author_email="vekariyajenil888@gmail.com",
    description="SDK for interacting with Slips IDS components",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jenilv-07/slips-sdk",
    packages=find_packages(include=["slips", "slips.*"]),
    include_package_data=True,
    python_requires=">=3.10",
    cmdclass={"install": CustomInstallCommand},
    entry_points={
        "console_scripts": [
            "slips-setup=slips.slips_setup:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
)
