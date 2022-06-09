from nltk.corpus import stopwords
from icrawler.builtin import GoogleImageCrawler
import nltk
import os, glob
import imageio
from PIL import Image
from gtts import gTTS
import moviepy.editor as mpe
import wikipedia
import nltk.data
from keybert import KeyBERT
user_input = 'bikes'
from moviepy.editor import *
import os
from natsort import natsorted

def delete_files(path):
    for f in os.listdir(path):
        os.remove(os.path.join(dir, f))

dir = r"C:\Users\miera\Desktop\cs338\TED-on-Demand\images"

filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)
nltk.download('stopwords')
nltk.download('punkt')

imageio.plugins.freeimage.download()
stopwords_dict = {word: 1 for word in stopwords.words("english")}
prompt = user_input
wiki_result = wikipedia.summary(prompt, sentences = 10)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = tokenizer.tokenize(wiki_result)
count = 0
kw_model = KeyBERT()

for sentence in sentences:
    delete_files(r"C:\Users\miera\Desktop\cs338\TED-on-Demand\images")
    print("sentence:", sentence,'\n\n\n\n\n\n\n\n\n\n\n\n')
    keywords = kw_model.extract_keywords(sentence)
    words = kw_model.extract_keywords(sentence, keyphrase_ngram_range=(1, 1), stop_words=None)
    queries = words[:3]
    filters = dict(
        type='photo'
        )
    final_query = ''
    for query in queries:
       final_query += query[0] + ' '   
    google_Crawler = GoogleImageCrawler(storage = {'root_dir': 'images'})
    google_Crawler.crawl(filters = filters,keyword = final_query, max_num = 1)    
    path = 'images'

    image_folder = os.fsencode(path)

    filenames = []

    for file in os.listdir(image_folder):
        filename = os.fsdecode(file)
        if filename.endswith( ('.jpg', '.png') ):
            filenames.append(os.path.join(path, filename))

    filenames.sort() 
    try:
        images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((512, 512)), filenames))
    except:
        os.rename(filenames[0],filenames[0][-3]+'.png')
        filenames[0] = filenames[0][-3]+'.png'
        images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((512, 512)), filenames))
    for i in range(len(images)):
        images[i] = images[i].convert("RGB")

    imageio.mimsave(os.path.join(path,'movieWorking.mp4'), images, fps=0.1)

    language = 'en'

    myobj = gTTS(text=sentence, lang=language, slow=False)

    myobj.save("background.mp3")

    movie_path = os.path.join(path,'movieWorking.mp4')
    audio_path = 'background.mp3'

    movie_clip = mpe.VideoFileClip(movie_path)
    audio_clip = mpe.AudioFileClip(audio_path)
    final_clip = movie_clip.set_audio(audio_clip)
    video_path = './videos/'+str(count)+'.mp4'
    final_clip.write_videofile(video_path)
    count+=1

L =[]

for root, dirs, files in os.walk(r"D:\Practicum\test\videos"):
    files = natsorted(files)
    for file in files:
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(root, file)
            video = VideoFileClip(filePath)
            L.append(video)

final_clip = concatenate_videoclips(L)
final_clip.to_videofile("output.mp4", remove_temp=True)
