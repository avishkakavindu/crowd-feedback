from builtins import input

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import LinearSVC
import string
from spacy.lang.en.stop_words import STOP_WORDS
import spacy
from csv import writer
from matplotlib import pyplot as plt
import seaborn as sns

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
columns_name = ['Review', 'Sentiment']

data_yelp = pd.read_csv('yelp_labelled.txt', sep='\t', header=None)
data_yelp.columns = columns_name

data_amazon = pd.read_csv('amazon_cells_labelled.txt', sep='\t', header=None)
data_amazon.columns = columns_name

data_imdb = pd.read_csv('imdb_labelled.txt', sep='\t', header=None)
data_imdb.columns = columns_name

Restaurant_Reviews = pd.read_csv('Restaurant_Reviews.tsv', sep='\t', header=None)
Restaurant_Reviews.columns = columns_name

# data = data_yelp.append([data_amazon, data_imdb, data_yelp, Restaurant_Reviews], ignore_index=True)
# Combine the DataFrames using concat
data = pd.concat([data_yelp, data_amazon, data_imdb, Restaurant_Reviews], ignore_index=True)

# # print(data.isnull().sum())
punct = string.punctuation

shop_lcation= str(input("Enter location number"))
user_comment= str(input("Enter your Comment about shop"))
product = str(input("Enter your Item id"))
# print(punct)

# //////////////////////////////////////////////////////////////////////////////////////
# save data to new location
def save_csv(location,comment,status,product):
    with open('event.csv', 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
        List = [location,comment,status,product]
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)

        # Close the file object
        f_object.close()


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


text_data_cleaning("Amazing app.I have been search this type of app for maintain my book collection . Very useful for home library owners. User friendly interfaces")

tfidf = TfidfVectorizer(tokenizer=text_data_cleaning)
classifier = LinearSVC()

X = data['Review']
y = data['Sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=420)

clf = Pipeline([('tfidf', tfidf), ('clf', classifier)])
clf.fit(X_train, y_train)

import joblib

model_filename = "sentiment_classifier_model.pkl"
joblib.dump(clf, model_filename)


y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Create a heatmap using seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()


# wrd1 = clf.predict(['Does not come with 3.5mm cord required to use on a pc, despite the description.Do not buy this if you need it for a pc. They are not shipping an Arctis model that comes with the cord, but rather one that is just for use with game systems.'])


wrd1 = clf.predict([user_comment])
# print(len(X))
# print(wrd1[0])
pr = str(wrd1[0])
if pr == '1':
    pr = 'Positive'
    print("Positive Comment")
    save_csv(shop_lcation, user_comment, str(wrd1[0]),product)


else:
    pr = 'Negative'
    print("Negative Comment")
    save_csv(shop_lcation, user_comment, str(wrd1[0]),product)

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
user_input = input("Enter your text: ")
result = predict_sentiment(user_input)
print("Feedback: ", result)



