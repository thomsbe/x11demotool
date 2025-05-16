from setuptools import setup, find_packages

setup(
    name="cliptool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Abhängigkeiten hier einfügen
    ],
    entry_points={
        'console_scripts': [
            'cliptool=cliptool.cli:main',
        ],
    },
    author="Thoms",
    description="Ein Tool zur Verwaltung von Zwischenablageninhalten",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
