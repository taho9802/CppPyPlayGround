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
    

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)
# fn = "code"
# ft = "mp3"
# audio_path = fn + "." + ft

audio_path = 'audio_files'
files = find_audio_files(audio_path, '.mp3')
selectedAudio, file_path_key = get_file_selection(files)
print(f'audio selected {selectedAudio} the key to file_path {file_path_key}')

audio = pydub.AudioSegment.from_mp3(selectedAudio.get(file_path_key))

segment_dir = segment_audio(audio)

for segment in segment_dir:
    os.remove(segment)