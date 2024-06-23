from cryptography.fernet import Fernet
import os
import hashlib
from mutagen.mp3 import MP3

def media_size(filepath):
    # size of audio file in bytes
    a_m_size = float(os.stat(filepath).st_size())
    mib_size = a_m_size/1048576.0
    return mib_size

def media_compression(filepath):
    return None

def extract_song_info(filepath):
  try:
    audio = MP3(filepath)
    metadata = {}
    # Extract title and artist
    metadata["title"] = audio.get("TIT2", None).text[0].decode("utf-8") if "TIT2" in audio else None
    metadata["artist"] = audio.get("TPE1", None).text[0].decode("utf-8") if "TPE1" in audio else None
    return metadata
  except (IOError, mutagen.error):
    print(f"Error accessing file: {filepath}")
    return None

def sha1_hash(data):
  sha1 = hashlib.sha1()
  sha1.update(data if isinstance(data, bytes) else data.encode())
  return sha1.digest()

def encrypt_file(key, input_file, output_file):
  with open(input_file, 'rb') as in_file, open(output_file, 'wb') as out_file:
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(in_file.read())
    out_file.write(encrypted_data)

list_of_files_path = '~/media/target'
list_of_files = os.listdir(list_of_files_path)

for i in list_of_files:
    filepath = list_of_files_path + "/" + str(i)
    if media_size > 25.0 :
        media_compression(filepath)
    title, artist = extract_song_info(filepath)
    key = sha1_hash((str(title) + "|" + str(artist)).encode())
    encrypted_file = list_of_files_path + "/encrypted/" key + ".encr"
    encrypt_audio(key, filepath, encrypted_file)
