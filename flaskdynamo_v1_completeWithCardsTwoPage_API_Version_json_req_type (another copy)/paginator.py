import boto3
i = 0
client = boto3.client('dynamodb')
paginator = client.get_paginator('scan')
print (paginator)
response_iterator = paginator.paginate(
    TableName="Movies",
    PaginationConfig={
        'MaxItems': 10,
        'PageSize': 5,
    }
)
# response_iterator['LastEvaluatedKey']
for page in response_iterator:
    print(page)
    while page['LastEvaluatedKey']:
        response_iterator = paginator.paginate(
            TableName="Movies",
            PaginationConfig={
                'MaxItems': 10,
                'PageSize': 5,
                'StartingToken':page['LastEvaluatedKey']
            }
        )


# while ['LastEvaluatedKey'] in response:
#     response = table.scan(
#     ProjectionExpression=pe,
#     FilterExpression=fe,
#     ExpressionAttributeNames= ean,
#     ExclusiveStartKey=response['LastEvaluatedKey']
#     )
    # i=i+1
# print(response_iterator)
# print(i)