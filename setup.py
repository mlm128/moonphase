from setuptools import setup, find_packages
import pathlib

# Read the contents of README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README_GITHUB.md").read_text(encoding="utf-8")

setup(
    name="moonphase-plus",
    version="2.0.0",
    description="Advanced moon phase calculator with beautiful visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/moonphase-plus",
    author="YG",
    author_email="your.email@example.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="moon, phase, astronomy, calculator, visualization",
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.8, <4",
    install_requires=[
        # Core dependencies
    ],
    extras_require={
        "gui": [
            "pillow>=9.0.0",
        ],
        "full": [
            "pillow>=9.0.0",
            "matplotlib>=3.5.0",
            "rich>=12.0.0",
        ],
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=0.990",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "moonphase=moonphase_final:main",
            "moonphase-gui=moonphase_modern:main",
            "moonphase-web=moonphase_web:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/moonphase-plus/issues",
        "Source": "https://github.com/YOUR_USERNAME/moonphase-plus",
        "Documentation": "https://github.com/YOUR_USERNAME/moonphase-plus/wiki",
    },
)