import setuptools

with open("README.md") as f:
    long_description = f.read()


setuptools.setup(
    name="dmerg",                     # This is the name of the package
    version="0.0.1",                  # The initial release version
    author="Nikolay Fedurko",         # Full name of the author
    description="Data merge from multiple formats to other formats(mainly json)",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    install_requires=[]                     # Install other dependencies if any
)
