from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

#  FinBERT pre-trained model and tokenizer
finbert_model = AutoModelForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = AutoTokenizer.from_pretrained('yiyanghkust/finbert-tone')

# Function to clean text and handle missing values
def clean_text(text):
    if isinstance(text, str):
        return text
    else:
        return ""  # Replace non-string or missing values with empty strings

# Apply the clean_text function to ensure all text fields are strings
data['Title'] = data['Title'].apply(clean_text)
data['Content'] = data['Content'].apply(clean_text)

# Modified sentiment score calculation using [-1, 1] range and weights
def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = finbert_model(**inputs)  
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1).numpy()
    
    # Weighted sentiment score: -1 for negative, 0 for neutral, +1 for positive
    sentiment_score = probs[0][2] - probs[0][0]  # (positive - negative) to get score between [-1, 1]
    return sentiment_score

# Apply sentiment analysis with weights (60% content, 40% title)
data['Title_Sentiment'] = data['Title'].apply(get_sentiment)
data['Content_Sentiment'] = data['Content'].apply(get_sentiment)

# Weighted average sentiment score: 60% content,40% title
data['Sentiment_Score'] = (0.6 * data['Title_Sentiment']) + (0.4 * data['Content_Sentiment'])

# Save the DataFrame with sentiment scores to a CSV file
data.to_csv('processed_stock_articles_with_sentiment_2016-23.csv', index=False)
