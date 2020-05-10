import json
from pathlib import Path

import boto3
import moto
import pytest

from dynamodb_ghost import ghost
from dynamodb_ghost.utils import subdict


@pytest.fixture
def mock_table_filename():
    return 'sample_table.json'


@pytest.fixture
def mock_table_details(mock_table_filename):
    with open(Path(__file__).parent.joinpath(mock_table_filename), 'r') as table_file:
        return json.load(table_file)


@pytest.fixture
def mock_ddb(mock_table_details):
    with moto.mock_dynamodb2():
        ddb_client = boto3.client('dynamodb')
        ddb_client.create_table(**mock_table_details)
        yield ddb_client


def test_ghost_yields_correct_name_when_specified(mock_ddb):
    with ghost(mock_ddb, 'mock_table', 'ghost_table') as ghost_name:
        assert ghost_name == 'ghost_table'


def test_ghost_yields_default_name_when_unspecified(mock_ddb):
    with ghost(mock_ddb, 'mock_table') as ghost_name:
        assert ghost_name == 'mock_table_ghost'


def test_ghost_is_deleted_after_manager_exists(mock_ddb):
    with ghost(mock_ddb, 'mock_table', wait=True) as _:
        pass
    ghost_table = boto3.resource('dynamodb').Table('mock_table_ghost')
    ghost_table.wait_until_not_exists()
    assert True


def test_ghost_has_same_attribute_definitions_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        assert ghost_table.attribute_definitions == mock_table_details['AttributeDefinitions']


@pytest.mark.skip(reason='Neither boto nor moto seem to return billing summary correctly...')
def test_ghost_has_same_billing_mode_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        assert ghost_table.billing_mode_summary['BillingMode'] == mock_table_details['BillingMode']


def test_ghost_has_same_key_schema_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        assert ghost_table.key_schema == mock_table_details['KeySchema']


def test_ghost_has_same_throughput_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        mock_table_throughput = mock_table_details['ProvisionedThroughput']
        assert ghost_table.provisioned_throughput['ReadCapacityUnits'] == mock_table_throughput['ReadCapacityUnits']
        assert ghost_table.provisioned_throughput['WriteCapacityUnits'] == mock_table_throughput['WriteCapacityUnits']


def test_ghost_has_same_stream_specification_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        assert ghost_table.stream_specification == mock_table_details['StreamSpecification']


def test_ghost_has_same_global_indexes_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        ghost_global_indexes = ghost_table.global_secondary_indexes
        assert len(ghost_global_indexes) == len(mock_table_details['GlobalSecondaryIndexes'])
        for index in ghost_global_indexes:
            index_spec = subdict(index, expected=['IndexName', 'KeySchema', 'Projection', 'ProvisionedThroughput'])
            assert index_spec in mock_table_details['GlobalSecondaryIndexes']


def test_ghost_has_same_local_indexes_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        ghost_local_indexes = ghost_table.local_secondary_indexes
        assert len(ghost_local_indexes) == len(mock_table_details['LocalSecondaryIndexes'])
        for index in ghost_local_indexes:
            index_spec = subdict(index, expected=['IndexName', 'KeySchema', 'Projection'])
            assert index_spec in mock_table_details['LocalSecondaryIndexes']


@pytest.mark.skip(reason='Not working currently')
def test_ghost_has_same_sse_specification_as_original(mock_ddb, mock_table_details):
    with ghost(mock_ddb, 'mock_table', wait=True) as ghost_name:
        ghost_table = boto3.resource('dynamodb').Table(ghost_name)
        assert ghost_table.sse_description['SSEType'] == mock_table_details['SSEType']
        assert ghost_table.sse_description['KMSMasterKeyArn'] == mock_table_details['KMSMasterKeyId']
