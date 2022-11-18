import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import os


# Create your views here.

def read_file(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def translate(input_text):
    import requests
    import uuid

    # Add your key and endpoint
    key = os.environ.get('TRANSLATE_KEY')
    endpoint = os.environ.get('TRANSLATE_ENDPOINT')
    location = os.environ.get('TRANSLATE_LOCATION')

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': 'zh'
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{"Text": input_text}]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return (response[0]["translations"][0]["text"])


@csrf_exempt
def image4analysis(request):
    if request.method == 'POST':
        img_input_object = request.FILES.get("img_input")
        images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
        local_image_path = os.path.join(images_folder, img_input_object.name)

        f = open(local_image_path, mode='wb')
        for chunk in img_input_object.chunks():
            f.write(chunk)
        f.close()

        subscription_key = os.environ.get('CV_KEY')
        endpoint = os.environ.get('CV_ENDPOINT')

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

        local_image = open(local_image_path, "rb")

        description_result = computervision_client.describe_image_in_stream(local_image)
        data = {
            "code": '200',
            "msg": '成功',
            "caption": description_result.captions[0].text,
            "caption-cn": translate(description_result.captions[0].text),
            "tags": description_result.tags,
        }
        print(data)
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')

    else:
        return HttpResponse('It is not a POST request!!!')
