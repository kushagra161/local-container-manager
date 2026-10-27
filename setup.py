from setuptools import setup, find_packages

setup(
    name="local-container-manager",
    version="1.0.0",
    author="Kushagra Kaushik",
    description="A beginner-friendly Docker container management CLI tool",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["docker>=6.1.3"],
    entry_points={
        "console_scripts": [
            "lcm=src.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Systems Administration",
    ],
)
