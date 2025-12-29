#!/usr/bin/env python3
"""
AEON Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aeon-engine",
    version="0.1.0",
    author="AEON Team",
    description="Autonomous Evolving Orchestration Network - A conscious context engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aeon",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "sentence-transformers>=2.2.2",
        "numpy>=1.24.3",
        "scipy>=1.11.4",
        "streamlit>=1.28.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "llm": [
            "openai>=1.3.0",
            "torch>=2.1.0",
            "transformers>=4.35.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aeon=run:main",
        ],
    },
)
