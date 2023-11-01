# Import necessary libraries
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import spacy
import numpy as np
import spacy
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load NLP models and dictionaries
nlp = spacy.load("en_core_web_sm")
sid = SentimentIntensityAnalyzer()

# Sample text for analysis
text = "I'm feeling so overwhelmed. It's hard to get out of bed in the morning, and I have no motivation."

# Tokenize and process the text
doc = nlp(text)

# Sentiment analysis
sentiment_score = sid.polarity_scores(text)

# Emotion analysis using TextBlob
emotion_blob = TextBlob(text)
emotion_polarity = emotion_blob.sentiment.polarity

# Linguistic features
word_count = len(doc)
average_word_length = np.mean([len(token) for token in doc if not token.is_punct])
sentence_count = len(list(doc.sents))

# Analyze the complexity of the text (you can use more sophisticated metrics)
complexity_score = word_count / sentence_count

# Machine learning-based mental health prediction (a simple classifier example)
# You would need a labeled dataset for training a classifier
# For this example, we use a dummy classifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Sample dataset (dummy data)
text_samples = ["I'm feeling great today.", "I'm feeling so sad and tired.", "I feel awesome!", "I'm struggling with life."]
labels = ["positive", "negative", "positive", "negative"]

# Vectorize the text data (you would need more advanced text features)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(text_samples)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train a classifier (you would need a more complex model for real-world data)
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Make predictions on the input text
predicted_label = classifier.predict(vectorizer.transform([text]))

# Display the results
print("Sentiment Score:", sentiment_score)
print("Emotion Polarity:", emotion_polarity)
print("Word Count:", word_count)
print("Average Word Length:", average_word_length)
print("Sentence Count:", sentence_count)
print("Text Complexity Score:", complexity_score)
print("Predicted Mental Health Label:", predicted_label[0])

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Sample text (you would replace this with the user's input)
text = """
I'm feeling really stressed out lately. I can't sleep at night, and my appetite has decreased significantly. 
I've lost interest in the things I used to enjoy. I feel hopeless and don't want to get out of bed in the morning.
"""

# Tokenize the text using spaCy
doc = nlp(text)

# Sentiment analysis using TextBlob
sentiment = TextBlob(text)
polarity = sentiment.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)

# Custom feature extraction and analysis
word_count = len(doc)
average_word_length = sum(len(token.text) for token in doc) / word_count
unique_words = len(set(token.text for token in doc))
noun_count = len([token for token in doc if token.pos_ == 'NOUN'])
verb_count = len([token for token in doc if token.pos_ == 'VERB'])
adjective_count = len([token for token in doc if token.pos_ == 'ADJ'])
adverb_count = len([token for token in doc if token.pos_ == 'ADV'])

# More advanced metrics would require a labeled dataset and machine learning

# Example machine learning with a hypothetical dataset
X, y = load_data()  # Load your labeled data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
classifier = RandomForestClassifier()
classifier.fit(X_train_tfidf, y_train)
y_pred = classifier.predict(vectorizer.transform(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Finally, you can combine all these metrics to assess the individual's mental health status and provide recommendations.
print("Sentiment Polarity:", polarity)
print("Word Count:", word_count)
print("Average Word Length:", average_word_length)
print("Unique Words:", unique_words)
print("Noun Count:", noun_count)
print("Verb Count:", verb_count)
print("Adjective Count:", adjective_count)
print("Adverb Count:", adverb_count)
