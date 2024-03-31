from openai import OpenAI
from dotenv import load_dotenv
import pydub
import os
import tempfile

load_dotenv()

def segment_audio(audio):
    segment_duration = 10 * 60 * 1000
    file_num = 0
    segment_dir = []
    temp_dir = 'audio_files/temp_file_storge'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    for start_index in range(0, len(audio), segment_duration):
        segment = audio[start_index:start_index+segment_duration]
        with tempfile.NamedTemporaryFile(delete=False, dir=temp_dir ,suffix=f'_{file_num}.mp3') as tmp_file:
            segment.export(tmp_file.name, format='mp3')
            segment_dir.append(tmp_file.name)
            file_num += 1
    return segment_dir

def find_audio_files(dir, ft):
    files = []
    for file in os.listdir(dir):
       if file.endswith(ft):
           new_dict = {}
           new_dict.update({file:os.path.join(dir,file)})
           files.append(new_dict)
    return files

def get_file_selection(files):
    print("List of files detected: ")
    for i, file in enumerate(files):
        print(f'[{i}]: {list(file.keys())[0]}')
    choice = int(input("Select which file you want: "))
    print(f'You have selected {files[choice]}')
    return files[choice], list(files[choice].keys())[0]

def transcribe_audio(file_dirs, client):
    final_transcription = ""
    for file_dir in file_dirs:
        audio_file = open(file_dir, 'rb')
        transcription = client.audio.transcriptions.create( model='whisper-1', file=audio_file)
        audio_file.close()
        final_transcription += transcription.text + "\n"
    return final_transcription
        

    

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)
# fn = "code"
# ft = "mp3"
# audio_path = fn + "." + ft

audio_path = 'audio_files'
files = find_audio_files(audio_path, '.mp3')
selectedAudio, title = get_file_selection(files)
print(f'audio selected {selectedAudio} the key to file_path {title}')

audio = pydub.AudioSegment.from_mp3(selectedAudio.get(title))

segment_dir = segment_audio(audio)

transcription = transcribe_audio(segment_dir, client)

with open(f'{title}_transcription.txt', 'w') as file:
    file.write(transcription)



for segment in segment_dir:
    os.remove(segment)