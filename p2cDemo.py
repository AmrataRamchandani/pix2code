from keras.models import model_from_json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import h5py as h5py
from compiler.classes.Compiler import *
from IPython.core.display import display,HTML
import sys
import pickle
import os

argv = sys.argv[1:]

if len(argv) < 1:
    print("Error: not enough argument supplied:")
    print("p2cDemo.py <image_path> path> ")
    exit(0)
else:
    image_path = argv[0]

#load model and weights
json_file = open('static/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("static/weights.h5")
print("Loaded model from disk")

# Read a file and return a string
def load_doc(filename):
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

# Initialize the function to create the vocabulary
tokenizer = Tokenizer(filters='', split=" ", lower=False)
# Create the vocabulary
tokenizer.fit_on_texts([load_doc('static/bootstrap.vocab')])

# map an integer to a word
def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

max_length = 48

# generate a description for an image
def generate_desc(model, tokenizer, photo, max_length):
    photo = np.array([photo])
    # seed the generation process
    in_text = '<START> '
    # iterate over the whole length of the sequence
    print('\nPrediction---->\n\n<START> ', end='')
    for i in range(150):
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = loaded_model.predict([photo, sequence], verbose=0)
        # convert probability to integer
        yhat = np.argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += word + ' '
        # stop if we predict the end of the sequence
        print(word + ' ', end='')
        if word == '<END>':
            break
    return in_text

# Converting Image to array
import cv2
img = cv2.imread(image_path)
img = cv2.resize(img, (256, 256))
img = img.astype('float32')
img /= 255

predictedd=[]
yhatt = generate_desc(loaded_model, tokenizer, img, max_length)
predictedd.append(yhatt.split())
# print(predictedd)
base=os.path.basename(image_path)
htmlfname=os.path.splitext(base)[0]

print(htmlfname)

#Compile the tokens into HTML and css
dsl_path = "compiler/assets/web-dsl-mapping.json"
compiler = Compiler(dsl_path)
compiled_website = compiler.compile(predictedd[0], "templates/index.html")

compiledwebsite = open('compiledwebsite.txt', 'w+')
compiledwebsite.write(compiled_website)
compiledwebsite.close()
