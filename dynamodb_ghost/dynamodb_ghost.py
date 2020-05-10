from contextlib import contextmanager

from dynamodb_ghost.utils import table_specification_from_description


@contextmanager
def ghost(boto_client, table_name, ghost_name=None, wait=False):
    """Creates and manages a DynamoDB ghost table.

    Creates a 'ghost' of an existing DynamoDB table -- a transient, empty copy
    containing the same metadata as the original.

    Args:
        boto_client: The boto client to use for creating the ghost copy.
        table_name: The name of the table we wish to create a ghost copy of.
        ghost_name: Optional name for the ghost copy.
        wait: Optional bool indicating whether to wait for creation.

    Yields:
        The name of the ghost copy. Defaults to '<table_name>_ghost' if not specified
        as an argument.
    """
    ghost_name = ghost_name if ghost_name is not None else f'{table_name}_ghost'
    table_description = boto_client.describe_table(TableName=table_name)['Table']
    ghost_specification = table_specification_from_description(table_description)
    ghost_specification['TableName'] = ghost_name
    boto_client.create_table(**ghost_specification)
    if wait:
        boto_client.get_waiter('table_exists').wait(TableName=ghost_name)
    yield ghost_name
    boto_client.delete_table(TableName=ghost_name)
