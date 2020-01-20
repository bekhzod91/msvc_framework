import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msvc_framework",
    version="0.0.1",
    author="Bekhzod Tillakhanov",
    author_email="bekhzod.tillakhanov@gmail.com",
    description="Microservice for django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myrubapa/msvc_framework",
    install_requires=['Django', 'djangorestframework'],
    python_requires=">=3.5",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
