"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
import re
import sys
from google.cloud import texttospeech
from google.cloud import texttospeech_v1
import xml.etree.ElementTree as ET

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"spiritual-oxide-391005-7f751364d56e.json"

### CONFIGS #######
voice = texttospeech_v1.VoiceSelectionParams(
    language_code="en-US"
)

# Select the type of audio file you want returned
audio_config = texttospeech_v1.AudioConfig(
    # https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1#audioencoding
    audio_encoding=texttospeech_v1.AudioEncoding.MP3,
    speaking_rate=0.77
)
###################

# Checks for validity of ssml syntax
def is_valid_xml(xml_string):
    try:
        # Try parsing the XML string
        ET.fromstring(xml_string)
        return True
    except ET.ParseError as e:
        print(e)
        return False

# Remove "Teacher:" and "Student:" prefixes from the SSML input
def remove_teacher_student(text):
    pattern = r'(Teacher:|Student:)'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

# Get rid of unnecessary whitespaces, newlines and tabs
# in the xml file to reduce size of API request
def xml_remove_whitespaces(text):
    return re.sub('\s+(?=<)', '', text)

def text_to_speech(client, path):
    with open(path, 'rb') as file:
        xml_data = file.read().decode('utf-8')

    if not is_valid_xml(xml_data):
        print("SSML parsing failed! Quitting..")
        return

    ssml = xml_remove_whitespaces(xml_data)
    ssml = remove_teacher_student(ssml)

    if not is_valid_xml(ssml):
        print("SSML parsing failed! Quitting..")
        return

    #print('Input = ', ssml)
    print('Length = ' + str(len(ssml)))

    synthesis_input = texttospeech_v1.SynthesisInput(ssml=ssml)

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    output_path = os.path.splitext(path)[0] + ".mp3"
    print(output_path)
    with open(output_path, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {output_path}')

def main():
    # Instantiates a client
    client = texttospeech_v1.TextToSpeechClient()

    folder_path = "german"

    # Parse arguments
    if len(sys.argv) == 1:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".xml"):
                file_path = os.path.join(folder_path, file_name)
                print("Processing " + file_name + "..")
                text_to_speech(client, file_path)
    elif len(sys.argv) == 2:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".xml") and file_name.startswith(sys.argv[1]):
                file_path = os.path.join(folder_path, file_name)
                print("Processing " + file_name + "..")
                text_to_speech(client, file_path)

    
    print("Program terminating")
   

if __name__ == '__main__':
    main()