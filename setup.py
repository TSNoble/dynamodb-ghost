from setuptools import setup, find_packages
from pathlib import Path

version = '0.0.1'
here = Path(__file__).parent.resolve()

with open(here.joinpath('README.md'), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='dynamodb_ghost',
    version=version,
    description='Create transient, metadata-preserving copies of DynamoDB tables.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TSNoble/dynamodb-ghost',
    author='Tom Noble',
    author_email='t.s.noble@outlook.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='aws dynamodb boto3 python',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=['boto3'],
    project_urls={
        'Bug Reports': 'https://github.com/TSNoble/dynamodb-ghost/issues',
        'Source': 'https://github.com/TSNoble/dynamodb-ghost',
    }
)
