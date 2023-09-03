import joblib
from builtins import input
import string
from spacy.lang.en.stop_words import STOP_WORDS
import spacy

model_filename = "sentiment_classifier_model.pkl"
stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
punct = string.punctuation


def text_data_cleaning(sentence):
    doc = nlp(sentence)
    tokens = []
    for token in doc:
        if token.lemma_ != "-PRON-":
            temp = token.lemma_.lower().strip()
        else:
            temp = token.lower_
        tokens.append(temp)

    cleaned_tokens = []
    for token in tokens:
        if token not in stopwords and token not in punct:
            cleaned_tokens.append(token)
    # print(cleaned_tokens, "clened tokens")
    return cleaned_tokens


# Function for inference
def predict_sentiment(text):
    # Load the saved model
    loaded_model = joblib.load(model_filename)
    # Use the model to make predictions
    prediction = loaded_model.predict([text])
    if prediction[0] == 1:
        return "Positive"
    else:
        return "Negative"


# Example usage of the inference function
# user_input = input("Enter your text: ")
# result = predict_sentiment(user_input)
# print("Feedback: ", result)
#
