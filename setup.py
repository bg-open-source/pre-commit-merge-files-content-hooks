from setuptools import setup, find_packages

name = 'pre_commit_merge_content_hooks'
version = '1.0.0'
description = 'pre-commit hooks for merging content from different files to one'

# Package dependencies
dependencies = [
    "pytest==7.3.1",
    "Faker==18.9.0",
]

# Package setup
setup(
    name=name,
    version=version,
    description=description,
    packages=find_packages(),
    install_requires=dependencies
)
