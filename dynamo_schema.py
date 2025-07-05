import boto3
from botocore.exceptions import ClientError

# create the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # change region if needed

# define the table name
table_name = 'PokemonCollection'

def create_pokemon_table():
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'name',
                    'KeyType': 'HASH'        # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'     # S = String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        print("Creating table...")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table '{table_name}' created successfully.")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{table_name}' already exists.")
        else:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    create_pokemon_table()
