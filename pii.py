import os, requests, uuid, json

import yaml

with open("config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Config read successful")
#print(config)

# Don't forget to replace with your Cog Services subscription key!
subscription_key = config[0]['azure']['subscription_key']

def get_pii(input_text, input_language):
    base_url = 'https://westus2.api.cognitive.microsoft.com/text/analytics'
    #path = '/v3.0/entities/recognition/general'
    #path = '/v3.1-preview.1/entities/recognition/pii?domain=phi&model-version=2020-04-01'
    #path = '/v3.1-preview.1/entities/recognition/pii?domain=phi'
    path = '/v3.1-preview.1/entities/recognition/pii'
    constructed_url = base_url + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = {
        'documents': [
            {
                'language': input_language,
                'id': '1',
                'text': input_text
            }
        ]
    }
    response = requests.post(constructed_url, headers=headers, json=body)
    return response.json()

text1 = "The patient's name is John Smith. He was born on 1 January 2021"
text2 = "His mobile is 07777888999"

pii = get_pii(text2, 'en')
print (pii)