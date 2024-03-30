from openai import OpenAI
from dotenv import load_dotenv
import pydub
import os

load_dotenv()

def find_audio_files(dir, ft):
    files = []
    for file in os.listdir(dir):
       if file.endswith(ft):
           new_dict = {}
           new_dict.update({file:os.path.join(dir,file)})
           files.append(new_dict)
    return files

def get_file_selection(files):
    print("Select which file you want to process:")
    for i, file in enumerate(files):
        print(f'[{i}]: {file}')
    

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=OPEN_AI_API_KEY)
# fn = "code"
# ft = "mp3"
# audio_path = fn + "." + ft

audio_path = 'audio_files'
files = find_audio_files(audio_path, '.mp3')
get_file_selection(files)