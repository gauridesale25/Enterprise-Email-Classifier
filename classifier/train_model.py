import pandas as pd
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
import joblib

# Sample data loading - replace with actual email data
data = pd.read_csv('classifier/emails.csv')  # Ensure you have a CSV file with columns 'subject', 'body', and 'is_spam'
data['text'] = data['subject'] + ' ' + data['body']

X = data['text']
y = data['is_spam']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions)}")

# Save the model
joblib.dump(model, 'email_classifier_model.pkl')
