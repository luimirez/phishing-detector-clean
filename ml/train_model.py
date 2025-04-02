import os
import pickle
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# It is time to load the dataset == Dataset==
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/phishing_email.csv')

try:
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip() #WE are going to remove leading/trailing spaces
except Exception as e:
    print(f"Failed to load dataset: {e}")
    exit()
    
#showing the cleaned column names to apply the debugging
print("Cleaned Columns:", df.columns.tolist())

print("Raw label values in CSV:")
print(df['label'].astype(str).str.lower().str.strip().unique())
    
#WE must clean the columns from the file
df = df[['text_combined', 'label']]
df = df.rename(columns={'text_combined': 'text'})

#Cleaning the data in use
df['text'] = df['text'].astype(str).str.strip()
#df['label'] = df['label'].astype(str).str.lower().str.strip()

# Just we need to convert into an integer — no need to map
df['label'] = pd.to_numeric(df['label'], errors='coerce')
df = df[df['label'].isin([0, 1])]


#valid_labels = {'phishing': 1, 'legitimate': 0}
#df = df[df['label'].isin(valid_labels.keys())]
#df['label'] = df['label'].map(valid_labels)

df = df[df['text'].str.len() > 0] #HERE is going to drop the empty emails not useful from the dataset

#We are going to make some verification, validation and the moment to train the model created
if df.empty:
    print("No valid rows after cleaning.")
    exit()
    
print(f"Training on {len(df)} emails")

#The use of pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
    ('clf', LogisticRegression(solver='liblinear'))
])

pipeline.fit(df['text'], df['label'])

#We have to save the model  from pipeline
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(pipeline, f)
    
print(f"Model trained and saved to: {MODEL_PATH}")