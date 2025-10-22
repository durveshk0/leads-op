import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle, os

# Load Data
df = pd.read_csv("data/leads.csv")
df = df.dropna(subset=["message", "final_label"])
print("✅ Loaded data:", df.shape)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["final_label"], test_size=0.2, random_state=42
)

# TF-IDF + Model
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Save combined pipeline
os.makedirs("models", exist_ok=True)
with open("models/trained_model.pkl", "wb") as f:
    pickle.dump((vectorizer, model), f)

print("✅ Model trained & saved as models/trained_model.pkl")
print("📈 Test Accuracy:", model.score(X_test_vec, y_test))
