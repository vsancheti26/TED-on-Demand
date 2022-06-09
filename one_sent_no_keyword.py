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

dir = 'C:/Users/miera/Desktop/cs338/TED-on-Demand/images'

filelist = glob.glob(os.path.join(dir, "*"))
for f in filelist:
    os.remove(f)
nltk.download('stopwords')
nltk.download('punkt')

stopwords_dict = {word: 1 for word in stopwords.words("english")}
prompt = user_input
wiki_result = wikipedia.summary(prompt, sentences = 10)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = tokenizer.tokenize(wiki_result)
count = 0
kw_model = KeyBERT()

for sentence in sentences:
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
    # google_Crawler.crawl(filters = filters,keyword = sentence, max_num = 1)         
    path = 'images'

    image_folder = os.fsencode(path)

    filenames = []

    for file in os.listdir(image_folder):
        filename = os.fsdecode(file)
        if filename.endswith( ('.jpg', '.png') ):
            filenames.append(os.path.join(path, filename))

    filenames.sort() 
    # for filename in filenames:
        
    #     print('filename',filename, imageio.imread(filename))
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
    #video_path = '/static/finalVid'+str(count)+'.mp4'
    video_path = './videos/'+str(count)+'.mp4'
    final_clip.write_videofile(video_path)
    count+=1