# Language Transfer GPT (German)
This project aims to be an extension of the German course by Mihalis Eleftheriou [Language Transfer](https://www.languagetransfer.org/). 
It is still a WIP. It has several salient features -
<li>Employs the Teaching Method to create high quality language courses</li>
<li>Created with the help of LLMs in a semi-automated fashion for quick and iterative development</li>
<li>Utilizes a text to speech cloud service for automatic creation of audio files</li>
<li>Formalize a way to create more courses like this in the future</li>

## Methodology
![image](https://github.com/abcdjdj/lt-gpt-german/assets/4457834/b83e84d8-4e48-4b77-8a97-1c413f3b9cdb)

The diagram above shows how LT-GPT courses are created. The steps are as follows
1. Use ChatGPT to generate an SSML (Speech Synthesis Markup Language) file containing a conversation between a student and a teacher. The input prompt can be an existing SSML file or course transcripts from Language Transfer (as an initial kickstarter)
2. Manually review the SSML file for errors, improvements and corrections.
3. Run `python ./app.py <lecture number>` to generate the mp3 file
4. Listen to generated MP3 and check if you are missing any pauses, or need to make alterations to make it feel more like Language Transfer.
5. Make corrections and go back to step 3. If it sounds good, you're all set!

## Setup Steps
1. Install [Python 3](https://www.python.org/downloads/)
2. Run `pip install google-cloud-texttospeech`
3. Create an account on Google Cloud
4. Download your text-to-speech private key [Tutorial](https://www.youtube.com/watch?v=ZXnPMzmrmIY&list=LL&index=113&t=98s)
5. Clone this repo - `https://github.com/abcdjdj/lt-gpt-german`
6. Place the json file in this folder
7. Change the private key file name in `app.py` at the top of the file
8. Run `python ./app.py` to generate all mp3 files
