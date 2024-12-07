import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SERVICE_REGION")

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

ssml_string = f"""
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
    <voice name='en-IE-ConnorNeural'>
        Hello, this is a test for Azure Text-to-Speech.
    </voice>
</speak>
"""

# If you would prefer to use prosody:

# ssml_string = f"""
# <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
#     <voice name='en-IE-RyanNeural'>
#         <break time='1s' />
#         <prosody rate='-10%' pitch='-5%'>
#             Hello, this is a test for Azure Text-to-Speech.
#         </prosody>
#     </voice>
# </speak>
# """

result = synthesizer.speak_ssml_async(ssml_string).get()
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    with open("local_output3.wav", "wb") as audio_file:
        audio_file.write(result.audio_data)
else:
    print(f"Error: {result.reason}")
