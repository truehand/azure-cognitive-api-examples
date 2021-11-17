from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

import yaml

with open("config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Config read successful")
#print(config)

endpoint = config[0]['azure']['text_endpoint']
key = AzureKeyCredential(config[0]['azure']['text_key'])

text_analytics_client = TextAnalyticsClient(endpoint, key)

## Detect language
print ("Detect language")
documents = [
    "I was born in Seattle.",
    "I grew up in London."
]

response = text_analytics_client.detect_language(documents)
result = [doc for doc in response if not doc.is_error]

for doc in result:
    print("Language: {}".format(doc))


## Analyze sentiment
print ("Sentiment analysis")
documents = [
    {"id": "1", "language": "en", "text": "I hated the movie. It was so boring!"},
    {"id": "2", "language": "en", "text": "The movie made it into my top ten favorites."},
    {"id": "3", "language": "en", "text": "What a great movie!"}
]

response = text_analytics_client.analyze_sentiment(documents, language="en")
result = [doc for doc in response if not doc.is_error]

for doc in result:
    print("Overall sentiment: {}".format(doc.sentiment))
    print("Scores: positive={}; neutral={}; negative={} \n".format(
        doc.confidence_scores.positive,
        doc.confidence_scores.neutral,
        doc.confidence_scores.negative,
    ))

print ()
print ("Recognise linked entities")
documents = [
    "Albert Einstein came up with the general relativity theory in 1916, before he moved to the US.",
    "Easter Island, a Chilean territory, is a remote volcanic island in Polynesia."
]

response = text_analytics_client.recognize_linked_entities(documents, language="en")
result = [doc for doc in response if not doc.is_error]

for doc in result:
    for entity in doc.entities:
        print("Entity: {}".format(entity.name))
        print("URL: {}".format(entity.url))
        print("Data Source: {}".format(entity.data_source))
        for match in entity.matches:
            print("Confidence Score: {}".format(match.confidence_score))
            print("Entity as appears in request: {}".format(match.text))
    print()


## Extract key phrases
print("Extract key phrases")
documents = [
    "Redmond is a city in King County, Washington, United States, located 15 miles east of Seattle.",
    "I need to take my cat to the veterinarian.",
    "I will travel to South America in the summer."
]

response = text_analytics_client.extract_key_phrases(documents, language="en")
result = [doc for doc in response if not doc.is_error]

for doc in result:
    print(doc.key_phrases)
