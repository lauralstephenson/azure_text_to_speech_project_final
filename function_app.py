import azure.functions as func
import azure.cognitiveservices.speech as speechsdk
import logging
import os
import base64
from dotenv import load_dotenv

load_dotenv()

app = func.FunctionApp()

@app.function_name(name="TextToSpeech")
@app.route(route="TextToSpeech", methods=["POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        text = req_body.get('text')
        voice_name = req_body.get('voice', 'en-US-JennyNeural')  # Default voice if not provided
    except ValueError:
        logging.error("Invalid JSON received")
        return func.HttpResponse("Invalid JSON", status_code=400)

    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SERVICE_REGION")

    if not speech_key or not service_region:
        logging.error("Environment variables for Azure Speech Service are not set")
        return func.HttpResponse("Environment variables for Azure Speech Service are not set.", status_code=500)

    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        ssml_string = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='{voice_name}'>
                {text}
            </voice>
        </speak>
        """


        result = synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
            # Encode audio data as Base64 to return as text
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            return func.HttpResponse(audio_base64, mimetype="text/plain")  # Return Base64 as text
        else:
            logging.error(f"Speech synthesis failed: {result.reason}")
            return func.HttpResponse(f"Error: {result.reason}", status_code=500)
    
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return func.HttpResponse(f"Unexpected error: {e}", status_code=500)
