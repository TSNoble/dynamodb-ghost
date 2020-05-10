[![PyPI version](https://badge.fury.io/py/dynamodb-ghost.svg)](https://badge.fury.io/py/dynamodb-ghost)
[![Build Status](https://travis-ci.com/TSNoble/dynamodb-ghost.svg?branch=master)](https://travis-ci.com/TSNoble/dynamodb-ghost)
[![codecov](https://codecov.io/gh/TSNoble/dynamodb-ghost/branch/master/graph/badge.svg)](https://codecov.io/gh/TSNoble/dynamodb-ghost)

# DynamoDB Ghost

DynamoDB Ghost is a small Python library providing the ability to create transient, metadata-preserving copies of DynamoDB tables on AWS.

## Installation

As easy as pip.

```bash
pip install dynamodb-ghost
```

## Usage

The main intention of DynamoDB Ghost is to be used as a testing aid in cases where we wish to apply a set of tests to an existing table without making modifications to the original (e.g. as part of setup)

Using pytests fixtures, a sample test such as:
```python
import pytest
import boto3

@pytest.fixture
def my_table():
    return boto3.resource('dynamodb').Table('my_table')

def test_table(my_table):
    assert ...
```

insead becomes:
```python
import pytest
import boto3
from dynamodb_ghost import ghost

@pytest.fixture
def my_table():
with ghost(boto3.client('dynamodb'), 'my_table') as ghost_table:
    yield boto3.resource('dynamodb').Table(ghost_table)

def test_table(my_table):
    assert ...
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
