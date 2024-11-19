from setuptools import setup, find_packages

setup(
    name="interactive_row_viewer",
    version="0.1.0",
    description="An interactive row viewer for Jupyter notebooks with editable fields",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/interactive_row_viewer",
    packages=find_packages(),
    install_requires=[
        "ipywidgets>=7.0.0",
        "pandas>=1.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
