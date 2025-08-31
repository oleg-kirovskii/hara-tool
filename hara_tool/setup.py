from setuptools import setup, find_packages

setup(
    name="hara_tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'hazop=hara_tool.hazop:main',
        ],
    },
)