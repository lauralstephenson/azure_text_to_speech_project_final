import requests
import base64

# Replace with the correct URL for your Azure Function endpoint
url = "http://localhost:7071/api/TextToSpeech"
data = {
    "text": "Hello, this is a test for Azure Text-to-Speech.",
    "voice": "en-IE-ConnorNeural"
}

# Send the POST request to the Azure Function
response = requests.post(url, json=data)

if response.status_code == 200:
    # Decode the Base64 response and save it as a .wav file
    audio_data = base64.b64decode(response.text)
    with open("output.wav", "wb") as file:
        file.write(audio_data)
    print("Audio saved as output.wav")
else:
    print(f"Request failed with status {response.status_code}: {response.text}")
