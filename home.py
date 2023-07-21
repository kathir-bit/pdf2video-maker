import PyPDF3
from gtts import gTTS
import pdfplumber
from bing_image_downloader import downloader
from moviepy.editor import AudioFileClip, ImageClip
import os 
import shutil


#step 1 : convert text to audio file

file = input("Enter the input pdf file name : ")



book = open(file, 'rb')
pdfReader = PyPDF3.PdfFileReader(book)

pages = pdfReader.numPages

print("no. of pages ",pages)
finalText = ""
with pdfplumber.open(file) as pdf:
    for i in range(0, pages): 
        
        page = pdf.pages[i]
        try:
            text = page.extract_text()
        except Exception as e :
            print("Text Extraction error : ",i )
            print(e)
            continue

        finalText += text
     
        

tts = gTTS(finalText)

tts.save("speech.mp3")

#step 2 : download a random picture file from the internet :

query_string = file
 
downloader.download(query_string, limit=1, output_dir='images', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)


#step 3 : create the video file with audio and pictures : 

def add_static_image_to_audio(image_path, audio_path, output_path):
    """Create and save a video file to `output_path` after 
    combining a static image that is located in `image_path` 
    with an audio file in `audio_path`"""
    # create the audio clip object
    audio_clip = AudioFileClip(audio_path)
    # create the image clip object
    image_clip = ImageClip(image_path)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path)

try :
    add_static_image_to_audio(f"/home/kathiravan/Desktop/IT Hobby projects /images/{file}/Image_1.jpg","speech.mp3","output.mp4")

except Exception as e :
    add_static_image_to_audio(f"/home/kathiravan/Desktop/IT Hobby projects /images/{file}/Image_1.png","speech.mp3","output.mp4")
    print(e)
    

#now remove unnecessary files then move output file to safe folder 

cwd = os.getcwd()
try :
    os.remove(f"{cwd}/speech.mp3")
    
    shutil.rmtree(f"{cwd}/images")
except Exception as e :
    print(e)








