from setuptools import setup, find_packages

setup(
    name="orchestration-decorators",
    version="1.0.0",
    packages=find_packages(),
    package_dir={"": "."},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "psutil>=7.0.0",
        "typing-extensions>=4.0.0; python_version<'3.9'",
    ],
    extras_require={
        'redis': ['redis>=4.0.0'],
    },
)
