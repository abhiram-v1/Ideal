#!/usr/bin/env python3
"""
Setup script for PDF Converter App
A professional Jupyter Notebook to PDF converter with aesthetic styling
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jupyter-pdf-converter",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Professional Jupyter Notebook to PDF converter with aesthetic styling",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/jupyter-pdf-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jupyter-pdf-convert=ultimate_converter:main",
        ],
    },
    keywords="jupyter notebook pdf converter conversion aesthetic styling",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/jupyter-pdf-converter/issues",
        "Source": "https://github.com/yourusername/jupyter-pdf-converter",
        "Documentation": "https://github.com/yourusername/jupyter-pdf-converter#readme",
    },
)
