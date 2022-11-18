import os

import azure.cognitiveservices.speech as speechsdk
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

import json
import time
from pydub import AudioSegment

def read_file(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def mp3_to_wav(mp3_path, wav_path):
    song = AudioSegment.from_mp3(mp3_path)
    song.export(wav_path, format="wav")

def debug_text2speech(speech_synthesis_result, input_text):
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(input_text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(
                    cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


@csrf_exempt
def text2speech(request):
    now = str(int(round(time.time() * 1000)))
    if request.method == 'POST':
        input_json = request.POST
        input_text = input_json['text_input']
        audio_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")
        local_audio_path = os.path.join(audio_folder, now + ".wav")
        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        audio_config = speechsdk.audio.AudioOutputConfig(filename=local_audio_path)

        speech_config.speech_synthesis_voice_name = "zh-CN-XiaochenNeural"

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(input_text).get()
        debug_text2speech(speech_synthesis_result, input_text)

        response = StreamingHttpResponse(read_file(local_audio_path))
        response["Content-Type"] = "audio/wav"
        response["Content-Disposition"] = 'attachment; filename={0}'.format(now + ".wav")
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response
    else:
        return HttpResponse('It is not a POST request!!!')


@csrf_exempt
def speech2text(request):
    if request.method == 'POST':
        # <SpeechRecognitionWithFile>
        audio_input_object = request.FILES.get("audio_input")
        audio_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")
        local_audio_path = os.path.join(audio_folder, audio_input_object.name)
        f = open(local_audio_path, mode='wb')
        for chunk in audio_input_object.chunks():
            f.write(chunk)
        f.close()

        if audio_input_object.name[-3:] == 'mp3':
            local_audio_path_wav = os.path.join(audio_folder, audio_input_object.name[:-4]+".wav")
            mp3_to_wav(local_audio_path, local_audio_path_wav)
            local_audio_path = local_audio_path_wav

        speech_key, service_region = os.environ.get('SPEECH_KEY'), os.environ.get('SPEECH_REGION')
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        audio_config = speechsdk.audio.AudioConfig(filename=local_audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="zh-CN",
                                                       audio_config=audio_config)
        result = speech_recognizer.recognize_once()
        data = {
            "code": '200',
            "msg": '成功',
            "data": result.text
        }
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                                status='200', reason='success')
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
            return HttpResponse('ERROR:Something wrong with Input Audio File', status='403')
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
            return HttpResponse('ERROR:Something wrong with Input Audio File', status='403')
    else:
        return HttpResponse('ERROR:It is not a POST request!!!', status='403')


@csrf_exempt
def talk(request):
    if request.method == 'POST':
        input_json = request.POST
        input_text = input_json['text_input']

        endpoint = os.environ.get('LANG_ENDPOINT')
        credential = AzureKeyCredential(os.environ.get('LANG_KEY'))
        knowledge_base_project = os.environ.get('LANG_PROJECT')
        deployment = "production"

        client = QuestionAnsweringClient(endpoint, credential)
        with client:
            question = input_text
            output = client.get_answers(
                question=question,
                project_name=knowledge_base_project,
                deployment_name=deployment
            )
        data = {
            "code": '200',
            "msg": '成功',
            "input": question,
            "data": output.answers[0].answer
        }
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json", charset='utf-8',
                            status='200', reason='success')
    else:
        return HttpResponse('It is not a POST request!!!')


@csrf_exempt
def talk_audio(request):
    if request.method == 'POST':

        # talk configure
        input_json = request.POST
        input_text = input_json['text_input']

        endpoint = os.environ.get('LANG_ENDPOINT')
        credential = AzureKeyCredential(os.environ.get('LANG_KEY'))
        knowledge_base_project = os.environ.get('LANG_PROJECT')
        deployment = "production"

        client = QuestionAnsweringClient(endpoint, credential)
        with client:
            question = input_text
            output = client.get_answers(
                question=question,
                project_name=knowledge_base_project,
                deployment_name=deployment
            )

        # speech2text configure
        now = str(int(round(time.time() * 1000)))
        input_text = output.answers[0].answer
        audio_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")
        local_audio_path = os.path.join(audio_folder, now + ".wav")
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        audio_config = speechsdk.audio.AudioOutputConfig(filename=local_audio_path)

        speech_config.speech_synthesis_voice_name = "zh-CN-XiaochenNeural"

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(input_text).get()
        debug_text2speech(speech_synthesis_result, input_text)

        response = StreamingHttpResponse(read_file(local_audio_path))
        response["Content-Type"] = "audio/wav"
        response["Content-Disposition"] = 'attachment; filename={0}'.format(now + ".wav")
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response
    else:
        return HttpResponse('It is not a POST request!!!')
