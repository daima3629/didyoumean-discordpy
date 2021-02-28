import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="didyoumean-discordpy",
    version="0.2.0",
    author="daima3629",
    author_email="daima3629@usbc.be",
    description="A discord.py extension for command name suggestion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daima3629/didyoumean-discordpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)