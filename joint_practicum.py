from nltk.corpus import stopwords
from icrawler.builtin import GoogleImageCrawler
import nltk
import os
import imageio
from PIL import Image
from gtts import gTTS
import moviepy.editor as mpe

nltk.download('stopwords')

stopwords_dict = {word: 1 for word in stopwords.words("english")}
text = 'are humans getting faster'
text = " ".join([word for word in text.split() if word not in stopwords_dict])
filters = dict(
    type='photo'
    )
google_Crawler = GoogleImageCrawler(storage = {'root_dir': 'images'})
google_Crawler.crawl(filters = filters,keyword = text, max_num = 10)

path = 'images'

image_folder = os.fsencode(path)

filenames = []

for file in os.listdir(image_folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.jpg', '.png') ):
        
        filenames.append(os.path.join(path, filename))

filenames.sort() 

images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((512, 512)), filenames))

for i in range(len(images)):
    images[i] = images[i].convert("RGB")

imageio.mimsave(os.path.join(path,'movieWorking.mp4'), images, fps=0.5) # modify duration as needed

mytext = 'Are humans getting faster?'

language = 'en'
  
myobj = gTTS(text=mytext, lang=language, slow=False)
  
myobj.save("background.mp3")

movie_path = os.path.join(path,'movieWorking.mp4')
audio_path = 'background.mp3'

movie_clip = mpe.VideoFileClip(movie_path)
audio_clip = mpe.AudioFileClip(audio_path)
final_clip = movie_clip.set_audio(audio_clip)
final_clip.write_videofile("finalVid.mp4")