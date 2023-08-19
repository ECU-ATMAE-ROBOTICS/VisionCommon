from setuptools import setup

setup(
    name="VisionCommon",
    version="0.1",
    author="Jarred",
    author_email="",
    description="Common Package for robotic visual needs",
    packages=["VisionCommon"],
    install_requires=[
        "iniconfig",
        "numpy",
        "opencv-python",
        "packaging",
        "pluggy",
        "pyzbar",
    ],
)
