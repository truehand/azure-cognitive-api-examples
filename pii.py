import os, requests, uuid, json
import yaml
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

with open("config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Config read successful")
#print(config)

# Don't forget to replace with your Cog Services subscription key!
subscription_key = config[0]['azure']['subscription_key']
endpoint = config[0]['azure']['text_endpoint']
key = config[0]['azure']['text_key']
print(key)

# Authenticate the client using your key and endpoint 
def authenticate_client(key, endpoint):
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client(key, endpoint)

def get_pii(client, documents, input_language):
    response = client.recognize_pii_entities(documents, language="en")
    result = [doc for doc in response if not doc.is_error]
    for doc in result:
        print("Redacted Text: {}".format(doc.redacted_text))
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print("\tCategory: {}".format(entity.category))
            print("\tConfidence Score: {}".format(entity.confidence_score))
            print("\tOffset: {}".format(entity.offset))
            print("\tLength: {}".format(entity.length))

text1 = [
    "The patient's name is John Smith. He was born on 1 January 2021",
    "His mobile is 07777 888999"
]

pii_analysis1 = get_pii(client, text1, 'en')