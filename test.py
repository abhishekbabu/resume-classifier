import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.corpus import stopwords
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import string
import re
import pickle

setofStopWords = set(stopwords.words('english')+['``',"''"])

def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    resumeText = resumeText.lower()  # convert to lowercase
    resumeTextTokens = word_tokenize(resumeText)  # tokenize
    filteredText = [w for w in resumeTextTokens if not w in setofStopWords]  # remove stopwords
    return ' '.join(filteredText)

cleaned_input = cleanResume(sys.argv[1])

max_length = 200
trunc_type = 'post'
padding_type = 'post'

with open('tokenizer/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('tokenizer/label_tokenizer.pickle', 'rb') as handle:
    label_tokenizer = pickle.load(handle)

predict_sequences = tokenizer.texts_to_sequences([cleaned_input])
predict_padded = pad_sequences(predict_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
predict_padded = np.array(predict_padded)

model = keras.models.load_model('model')
prediction = model.predict(predict_padded)

predict_label = label_tokenizer.sequences_to_texts(prediction)
print(predict_label)

#print(predict_padded)
#print(cleaned_input)
#print(prediction)