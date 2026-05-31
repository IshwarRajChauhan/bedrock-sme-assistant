import json
import boto3

client_sme = boto3.client('bedrock-runtime')
def lambda_handler(event, context):
    user_input = event['prompt']
    print(user_input)

    #1. Create the message prompt for the model
    message_prompt = [
    {
        "role": "user",
        "content": [
            {
                "text": user_input
            }
        ]
    }
]

    #2. Create the system prompt for the model
    system_prompt = [
        {
            "text": "Act as a wind turbine manufacturing assistant. Summarize the logs in 5 lines."
        }
    ]

    #3. Create the inference parameters for the model
    inference_params = {
        "maxTokens": 2500,
        "topP": 0.9,
        "topK": 20,
        "temperature": 0.7,
    }


    #4. Create the request body for the model invocation
    request_body = {
        "schemaVersion": "messages-v1",
        "messages": message_prompt,
        "system": system_prompt,
        "inferenceConfig": inference_params,
    }
    

    #5. Invoke the model and get the response
    response = client_sme.invoke_model(
        body=json.dumps(request_body),
        contentType='application/json',
        accept='application/json',
        modelId='apac.amazon.nova-pro-v1:0',
        guardrailIdentifier='hmszjawjyp34',
        guardrailVersion='1',
        trace='ENABLED',
        performanceConfigLatency='standard'
    )



    #6. Parse the response and return the final output
    response_dict = json.loads(response['body'].read())
    final_response = response_dict["output"]["message"]["content"][0]["text"]
    #print(final_response)
    #print(type(response_dict))


    #7. Return the final response to the user
    return {
        'statusCode': 200,
        'body': json.dumps(final_response)
    }
