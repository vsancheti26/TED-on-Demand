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

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)

# home page of our site
@app.route("/")  
def home():
	return render_template("index.html") 

@app.route('/', methods = ['POST'])
def form_post():
	user_input = request.form['promptInput']
	
	# start of processing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
	print("sentence:", sentences[0])
	count = 0
	for sentence in sentences:
		sentence = " ".join([word for word in sentence.split() if word not in stopwords_dict])
		filters = dict(
			type='photo'
			)
		google_Crawler = GoogleImageCrawler(storage = {'root_dir': 'images'})
		google_Crawler.crawl(filters = filters,keyword = sentence, max_num = 5)
		
		# trying to fix image naming issue
		# select newly added imgs
		file_path = 'C:/Users/miera/Desktop/cs338/TED-on-Demand/images/0000'
		final_file_paths = []
		for i in range(1,6):
			if i!=10:
				final_file_path = file_path + '0' + str(i) + '.jpg'
			else:
				final_file_path = file_path + str(i) + '.jpg'
			final_file_paths.append(final_file_path)
		#for new imgs rename them 
		for i in range(len(final_file_paths)):
			try:
				new_name = final_file_paths[i][:-5] + str(count) +'_new_'+ '.jpg'
				print('NEW NAME IS: ',new_name)
				count+=1
				os.rename(final_file_paths[i], new_name)
				

			except:
				new_name = final_file_paths[i][:-5] + str(count)+'_new_' + '.png'
				print('png old name',final_file_paths[i] )
				print('png NEW NAME IS: ',new_name)
				count+=1
				os.rename(final_file_paths[i][:-3]+'png', new_name)
				

		

	path = 'images'

	image_folder = os.fsencode(path)

	filenames = []

	for file in os.listdir(image_folder):
		filename = os.fsdecode(file)
		if filename.endswith( ('.jpg', '.png') ):
			filenames.append(os.path.join(path, filename))

	filenames.sort() 
	for filename in filenames:
		print('filename',filename, imageio.imread(filename))
	images = list(map(lambda filename: Image.fromarray(imageio.imread(filename)).resize((512, 512)), filenames))

	for i in range(len(images)):
		images[i] = images[i].convert("RGB")

	imageio.mimsave(os.path.join(path,'movieWorking.mp4'), images, fps=0.1)

	language = 'en'
	
	myobj = gTTS(text=wiki_result, lang=language, slow=False)
	
	myobj.save("background.mp3")

	movie_path = os.path.join(path,'movieWorking.mp4')
	audio_path = 'background.mp3'

	movie_clip = mpe.VideoFileClip(movie_path)
	audio_clip = mpe.AudioFileClip(audio_path)
	final_clip = movie_clip.set_audio(audio_clip)
	final_clip.write_videofile("./static/finalVid.mp4")

	return render_template("result.html")