import requests
import json


def emotion_analyzer(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com" \
          "/instances/989792d2-1964-47da-9d41-874a5bab7f0e/v1/analyze?version=2019-07-12"

    api_key = "CBXLJQu3GuHt-RSGDLHyATTLilfDWs7yrBQzuO_1lTfb"

    headers = {
        'Content-Type': 'application/json'
    }

    data = '{"text":"' + text + '","features":{"emotion":{}}, "language": "en"}'

    response = requests.post(url, headers=headers, data=data, auth=('apikey', api_key))

    return json.loads(response.text)['emotion']['document']['emotion']


def text_to_speech(text, filename):
    url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com" \
          "/instances/dedf6abf-7700-49c9-8e72-bd9e39f6928f/v1/synthesize"

    api_key = "-r829qC-Rp46JkXmNNFG503q-S40cWMkzfCpgfxDRsuh"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg'
    }

    data = '{"text":"' + text + '"}'

    response = requests.post(url, headers=headers, data=data, auth=('apikey', api_key))

    with open(filename, 'wb') as f:
        f.write(response.content)



