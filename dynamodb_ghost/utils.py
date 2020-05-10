def table_specification_from_description(table_description):
    table_spec = subdict(table_description,
                         expected=['AttributeDefinitions', 'TableName', 'KeySchema'],
                         optional=['StreamSpecification'])
    if 'ProvisionedThroughput' in table_description:
        table_spec['ProvisionedThroughput'] = throughput_from_description(table_description['ProvisionedThroughput'])
    if 'LocalSecondaryIndexes' in table_description:
        table_spec['LocalSecondaryIndexes'] = [local_index_from_description(index) for index
                                               in table_description['LocalSecondaryIndexes']]
    if 'GlobalSecondaryIndexes' in table_description:
        table_spec['GlobalSecondaryIndexes'] = [global_index_from_description(index) for index
                                                in table_description['GlobalSecondaryIndexes']]
    if 'BillingModeSummary' in table_description:
        table_spec['BillingMode'] = billing_mode_from_summary(table_description['BillingModeSummary'])
    if 'SSEDescription' in table_description:
        table_spec['SSESpecification'] = sse_specification_from_description(table_description['SSEDescription'])
    return table_spec


def local_index_from_description(index_description):
    """Builds a LocalSecondaryIndex object from a LocalSecondaryIndexDescription object.

        - IndexArn [-]
        - IndexSizeBytes [-]
        - ItemCount [-]

    Args:
        A LocalSecondaryIndexDescription object (e.g. returned by DescribeTable action).

    Returns:
        A LocalSecondaryIndex object containing the same info.
    """
    return subdict(index_description, expected=['IndexName', 'KeySchema', 'Projection'])


def global_index_from_description(index_description):
    """Builds a GlobalSecondaryIndex object from a GlobalSecondaryIndexDescription object.

        - Backfilling [-]
        - IndexArn [-]
        - IndexSizeBytes [-]
        - IndexStatus [-]
        - ItemCount [-]

    Args:
        index_description: A GlobalSecondaryIndexDescription object (e.g. returned by DescribeTable action).

    Returns:
        A GlobalSecondaryIndex object containing the same info.
    """
    index_params = subdict(index_description, expected=['IndexName', 'KeySchema', 'Projection'])
    if 'ProvisionedThroughput' in index_description:
        index_params['ProvisionedThroughput'] = throughput_from_description(index_description['ProvisionedThroughput'])
    return index_params


def throughput_from_description(throughput_description):
    """Builds a ProvisionedThroughput object from a ProvisionedThroughputDescription object.

        - LastDecreaseDatetime [-]
        - LastIncreaseDatetime [-]
        - NumberOfDecreasesToday [-]

    Args:
        throughput_description: A ProvisionedThroughputDescription object (e.g. returned by DescribeTable action).

    Returns:
        A ProvisionedThroughput object containing the same info.
    """
    return subdict(throughput_description, expected=['ReadCapacityUnits', 'WriteCapacityUnits'])


def sse_specification_from_description(sse_description):
    """Builds an SSESpecification object from an SSEDescription object.

        - Status: str -> Enabled: bool
        - KMSMasterKeyArn -> KmsMasterKeyId
        - InaccessibleEncryptionDateTime [-]

    Args:
        sse_description: An SSEDescription object (e.g. returned by DescribeTable action).

    Returns:
        An SSESpecification object containing the same info.
    """
    sse_params = subdict(sse_description, optional=['SSEType'])
    sse_params['Enabled'] = True if sse_description['Status'] == 'ENABLED' else False
    if 'KMSMasterKeyArn' in sse_description:
        sse_params['KMSMasterKeyId'] = sse_description['KMSMasterKeyArn']
    return sse_params


def billing_mode_from_summary(billing_mode_summary):
    """Extract BillingMode field from BillingModeSummary object."""
    return billing_mode_summary["BillingMode"]


def subdict(dict, expected=[], optional=[]):
    for field in expected:
        if field not in dict:
            raise ValueError(f'Field "{field}" expected')
    return {key: value for key, value in dict.items() if key in [*expected, *optional]}
