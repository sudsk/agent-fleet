from setuptools import setup, find_packages

setup(
    name="agentfleet-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "requests>=2.25.0",
        "pyyaml>=6.0",
        "colorama>=0.4.4",
        "tabulate>=0.8.9",
    ],
    entry_points={
        "console_scripts": [
            "agentfleet=agentfleet_cli.cli:main",
        ],
    },
    author="Suds Kumar",
    author_email="info@agentfleet.io",
    description="CLI tool for integrating with AgentFleet.io",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sudsk/agent-fleet",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
