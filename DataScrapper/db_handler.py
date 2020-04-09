from boto3 import resource
from boto3.dynamodb.conditions import Key

def add_item(mapping, table_name="nyc_restaurant_inspection"):
    """
    Add one item (row) to table. mapping is a dictionary {col_name: value}.
    will overwrite if the item exist
    """
    table = resource('dynamodb').Table(table_name)
    response = table.put_item(Item=mapping)
    return response

