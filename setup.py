from setuptools import setup, find_packages

setup(
    name="dj_notification",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[

    ],
    description="notificatio app",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Arezoo Darvishi",
    author_email="arezoo.darvish6969@gmail.com",
    url="https://github.com/Oxalisystech/Notification",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)