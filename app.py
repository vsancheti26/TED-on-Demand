from flask import Flask
from flask import render_template, request, redirect, url_for

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
from keytotext import trainer
import wikipedia

from keytotext import trainer
import wikipedia
from gtts import gTTS
import moviepy.editor as mpe

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
from rpunct import RestorePuncts



app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

# home page of our site
@app.route("/")  
def home():
	return render_template("index.html") 

@app.route('/wiki_result', methods = ['POST'])
def form_post():
	user_input = request.form['promptInput']
	
	# start of processing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def delete_files(path):
		for f in os.listdir(path):
			os.remove(os.path.join(dir, f))

	dir = r"C:\Users\miera\Desktop\cs338\TED-on-Demand\images"

	filelist = glob.glob(os.path.join(dir, "*"))
	for f in filelist:
		os.remove(f)


	imageio.plugins.freeimage.download()
	stopwords_dict = {word: 1 for word in stopwords.words("english")}
	prompt = user_input
	wiki_result = wikipedia.summary(prompt, sentences = 10)
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = tokenizer.tokenize(wiki_result)
	count = 0
	kw_model = KeyBERT()

	for sentence in sentences:
		delete_files(dir)
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
			images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((1280, 720)), filenames))
		except:
			try:
				old_name = filenames[0]
				new_name = filenames[0][:-3]+'png'
				os.rename(old_name,new_name)
				filenames[0] = filenames[0][:-3]+'png'
				images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((1280, 720)), filenames))
			except:
				continue

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

	for root, dirs, files in os.walk(r'C:\Users\miera\Desktop\cs338\TED-on-Demand\videos'):
		files = natsorted(files)
		for file in files:
			if os.path.splitext(file)[1] == '.mp4':
				filePath = os.path.join(root, file)
				video = VideoFileClip(filePath)
				L.append(video)

	final_clip = concatenate_videoclips(L)
	final_clip.to_videofile("./static/finalVid.mp4", remove_temp=True)

	return render_template("result.html", prompt=prompt)


def resizeImgs(filename):
	try:
		return Image.fromarray(imageio.imread(filename)).resize((512, 512))
	except:
		print('issues w/ this file', filename)
		return

@app.route('/nlp_result', methods = ['POST'])
def nlp_form_post():
	# do processing here
	user_input = request.form['promptInput']
	imageio.plugins.freeimage.download()
	prompt = user_input

	intro_model = trainer()
	intro_model.load_model(r"C:\Users\miera\Desktop\cs338\TED-on-Demand\Intro_Model", use_gpu=False)

	keywords=prompt.split()
	intro = intro_model.predict(keywords,  use_gpu=False).strip() 
	rpunct = RestorePuncts()
	intro = rpunct.punctuate(intro)



	main_body = wikipedia.summary(prompt, sentences = 5).strip() 

	outro_model = trainer()
	outro_model.load_model(r'C:\Users\miera\Desktop\cs338\TED-on-Demand\Outro_Model', use_gpu=False)
	outro = outro_model.predict(keywords,  use_gpu=False).strip() 
	outro = rpunct.punctuate(outro)
	myobj = gTTS(text=intro, lang='en', slow=False)
	myobj.save("./content/intro.mp3")
	movie_clip = mpe.VideoFileClip('./content/loop.mp4')
	audio_clip = mpe.AudioFileClip('./content/intro.mp3')
	loopedClip = movie_clip.loop(duration = audio_clip.duration)
	loopedClip = loopedClip.set_audio(audio_clip)
	loopedClip.write_videofile('./videoParts/0final.mp4')

	myobj = gTTS(text=outro, lang='en', slow=False)
	myobj.save("./content/outro.mp3")
	movie_clip = mpe.VideoFileClip('./content/loop.mp4')
	audio_clip = mpe.AudioFileClip('./content/outro.mp3')
	loopedClip = movie_clip.loop(duration = audio_clip.duration)
	loopedClip = loopedClip.set_audio(audio_clip)
	loopedClip.write_videofile('./videoParts/2final.mp4')

	def delete_files(path):
		for f in os.listdir(path):
			os.remove(os.path.join(dir, f))

	dir = r"C:\Users\miera\Desktop\cs338\TED-on-Demand\images"

	filelist = glob.glob(os.path.join(dir, "*"))
	for f in filelist:
		os.remove(f)


	imageio.plugins.freeimage.download()
	stopwords_dict = {word: 1 for word in stopwords.words("english")}
	prompt = user_input
	wiki_result = wikipedia.summary(prompt, sentences = 10)
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	sentences = tokenizer.tokenize(wiki_result)
	count = 0
	kw_model = KeyBERT()

	for sentence in sentences:
		delete_files(dir)
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
			images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((1280, 720)), filenames))
		except:
			try:
				old_name = filenames[0]
				new_name = filenames[0][:-3]+'png'
				os.rename(old_name,new_name)
				filenames[0] = filenames[0][:-3]+'png'
				images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((1280, 720)), filenames))
			except:
				continue

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

	for root, dirs, files in os.walk(r'C:\Users\miera\Desktop\cs338\TED-on-Demand\videos'):
		files = natsorted(files)
		for file in files:
			if os.path.splitext(file)[1] == '.mp4':
				filePath = os.path.join(root, file)
				video = VideoFileClip(filePath)
				L.append(video)

	final_clip = concatenate_videoclips(L)
	final_clip.to_videofile("./videoParts/1final.mp4", remove_temp=True)

	L =[]

	for root, dirs, files in os.walk(r'C:\Users\miera\Desktop\cs338\TED-on-Demand\videoParts'):
		files = natsorted(files)
		for file in files:
			if os.path.splitext(file)[1] == '.mp4':
				filePath = os.path.join(root, file)
				video = VideoFileClip(filePath)
				L.append(video)

	final_clip = concatenate_videoclips(L)
	# final_clip.to_videofile("./static/finalVid.mp4", remove_temp=True)
	final_clip.write_videofile("./static/finalVid.mp4")


	return render_template("result.html")
