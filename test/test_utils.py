import pytest


from dynamodb_ghost.utils import sse_specification_from_description, throughput_from_description,\
    billing_mode_from_summary, global_index_from_description, local_index_from_description, \
    subdict


@pytest.fixture
def attribute_definitions():
    return [
        {
            "AttributeName": "key",
            "AttributeType": "S"
        },
        {
            "AttributeName": "local_index_key",
            "AttributeType": "S"
        },
        {
            "AttributeName": "global_index_key",
            "AttributeType": "S"
        }
    ]


@pytest.fixture
def key_schema():
    return [
        {
            "AttributeName": "key",
            "KeyType": "HASH"
        },
        {
            "AttributeName": "local_index_key",
            "KeyType": "RANGE"
        }
    ]


@pytest.fixture
def global_index_key_schema():
    return [
        {
            "AttributeName": "global_index_key",
            "KeyType": "HASH"
        }
    ]


@pytest.fixture
def sse_description_enabled():
    return {
        "Status": "ENABLED",
        "SSEType": "KMS",
        "KMSMasterKeyArn": "test",
        "InaccessibleEncryptionDatetime": "123"
    }


@pytest.fixture
def sse_description_disabled():
    return {
        "Status": "DISABLED"
    }


@pytest.fixture
def throughput_description():
    return {
        "LastDecreaseDatetime": "123",
        "LastIncreaseDatetime": "456",
        "NumberOfDecreasesToday": 1,
        "ReadCapacityUnits": 2,
        "WriteCapacityUnits": 3
    }


@pytest.fixture
def billing_mode_summary():
    return {
        "BillingMode": "PROVISIONED",
        "LastUpdateToPayPerRequestDateTime": "123"
    }


@pytest.fixture
def global_index_description(global_index_description_without_throughput, throughput_description):
    return dict(global_index_description_without_throughput, ProvisionedThroughput=throughput_description)


@pytest.fixture
def global_index_description_without_throughput(global_index_key_schema, index_projection):
    return {
        "IndexName": "global_index",
        "KeySchema": global_index_key_schema,
        "Projection": index_projection,
        "Backfilling": True,
        "IndexArn": "test",
        "IndexSizeBytes": 100,
        "IndexStatus": "CREATING",
        "ItemCount": 10
    }


@pytest.fixture
def local_index_description(key_schema, index_projection):
    return {
        "IndexName": "local_index",
        "KeySchema": key_schema,
        "Projection": index_projection,
        "IndexArn": "test",
        "IndexSizeBytes": 100,
        "ItemCount": 10
    }


@pytest.fixture
def index_projection():
    return {
        "ProjectionType": "INCLUDE",
        "NonKeyAttributes": ["index_value"]
    }


@pytest.fixture
def test_dict():
    return {'a': 1, 'b': 2, 'c': 3}


def test_sse_specification_with_sse_enabled(sse_description_enabled):
    expected = {
        "Enabled": True,
        "SSEType": "KMS",
        "KMSMasterKeyId": "test"
    }
    assert sse_specification_from_description(sse_description_enabled) == expected


def test_sse_specification_with_sse_disabled(sse_description_disabled):
    expected = {
        "Enabled": False
    }
    assert sse_specification_from_description(sse_description_disabled) == expected


def test_throughput_from_description(throughput_description):
    expected = {
        "ReadCapacityUnits": 2,
        "WriteCapacityUnits": 3
    }
    assert throughput_from_description(throughput_description) == expected


def test_billing_mode_from_summary(billing_mode_summary):
    assert billing_mode_from_summary(billing_mode_summary) == "PROVISIONED"


def test_global_index_from_description(global_index_description):
    expected = {
        "IndexName": "global_index",
        "KeySchema": [
            {
                "AttributeName": "global_index_key",
                "KeyType": "HASH"
            }
        ],
        "Projection": {
            "ProjectionType": "INCLUDE",
            "NonKeyAttributes": ["index_value"]
        },
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 2,
            "WriteCapacityUnits": 3
        }
    }
    assert global_index_from_description(global_index_description) == expected


def test_global_index_from_description_without_throughput(global_index_description_without_throughput):
    expected = {
        "IndexName": "global_index",
        "KeySchema": [
            {
                "AttributeName": "global_index_key",
                "KeyType": "HASH"
            }
        ],
        "Projection": {
            "ProjectionType": "INCLUDE",
            "NonKeyAttributes": ["index_value"]
        }
    }
    assert global_index_from_description(global_index_description_without_throughput) == expected


def test_local_index_from_description(local_index_description):
    expected = {
        "IndexName": "local_index",
        "KeySchema": [
            {
                "AttributeName": "key",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "local_index_key",
                "KeyType": "RANGE"
            }
        ],
        "Projection": {
            "ProjectionType": "INCLUDE",
            "NonKeyAttributes": ["index_value"]
        }
    }
    assert local_index_from_description(local_index_description) == expected


def test_subdict_with_no_elements_and_no_required(test_dict):
    assert subdict(test_dict, expected=[], optional=[]) == {}


def test_subdict_with_one_element_and_no_required(test_dict):
    assert subdict(test_dict, optional=['a']) == {'a': 1}
    assert subdict(test_dict, optional=['b']) == {'b': 2}
    assert subdict(test_dict, optional=['c']) == {'c': 3}


def test_subdict_with_one_element_and_required_satisfied(test_dict):
    assert subdict(test_dict, expected=['a']) == {'a': 1}
    assert subdict(test_dict, expected=['b']) == {'b': 2}
    assert subdict(test_dict, expected=['c']) == {'c': 3}


def test_subdict_with_two_elements_and_no_required(test_dict):
    assert subdict(test_dict, optional=['a', 'b']) == {'a': 1, 'b': 2}
    assert subdict(test_dict, optional=['b', 'c']) == {'b': 2, 'c': 3}
    assert subdict(test_dict, optional=['a', 'c']) == {'a': 1, 'c': 3}


def test_subdict_with_two_elements_and_required_satisfied(test_dict):
    assert subdict(test_dict, expected=['a', 'b']) == {'a': 1, 'b': 2}
    assert subdict(test_dict, expected=['b', 'c']) == {'b': 2, 'c': 3}
    assert subdict(test_dict, expected=['a', 'c']) == {'a': 1, 'c': 3}


def test_subdict_with_all_elements_and_no_required(test_dict):
    assert subdict(test_dict, optional=['a', 'b', 'c']) == test_dict


def test_subdict_with_all_elements_and_required_satisfied(test_dict):
    assert subdict(test_dict, expected=['a', 'b', 'c']) == test_dict


def test_subdict_with_requirements_unsatisfied(test_dict):
    with pytest.raises(ValueError):
        assert subdict(test_dict, expected=['d'])
    with pytest.raises(ValueError):
        assert subdict(test_dict, expected=['d'], optional=['a'])
    with pytest.raises(ValueError):
        assert subdict(test_dict, expected=['d'], optional=['a', 'b', 'c'])
