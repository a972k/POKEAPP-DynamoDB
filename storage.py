import boto3
from botocore.exceptions import ClientError

# dynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # change region if needed
table = dynamodb.Table('PokemonCollection')

# get a pokemon by name from dynamoDB
def get_pokemon(name):
    try:
        response = table.get_item(Key={'name': name})
        return response.get('Item')  # returns None if not found
    except ClientError as e:
        print(f"Error getting Pokémon: {e.response['Error']['Message']}")
        return None

# save a pokemon to dynamoDB
def save_pokemon(data):
    try:
        table.put_item(Item=data)
        print(f"Saved {data['name']} to DynamoDB.")
    except ClientError as e:
        print(f"Error saving Pokémon: {e.response['Error']['Message']}")
