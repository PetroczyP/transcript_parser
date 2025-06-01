# setup.py

from setuptools import setup, find_packages

setup(
    name="transcript-parser",
    version="1.0.0",
    description="A CLI tool to parse VTT-style transcripts into clean TXT/JSON",
    author="Peter Petroczy",
    url="https://github.com/PetroczyP/transcript_parser",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "transcript-parser = transcript_parser.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)