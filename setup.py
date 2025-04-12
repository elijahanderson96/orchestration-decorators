from setuptools import setup, find_packages

setup(
    name="orchestration-decorators",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=4.0.0; python_version<'3.9'",
    ],
)
