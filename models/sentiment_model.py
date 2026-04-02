import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax

# load sentimen hasil best model
@st.cache_resource
def load_sentiment_model():
    try:
        path = "sentiment_best_model"
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForSequenceClassification.from_pretrained(path)
        model.eval()
        return tokenizer, model
    except Exception as e:
        st.error(f"Gagal memuat model sentiment: {e}")
        return None, None

# label map dari sentimen
label_map_sentimen = {
    0: "Positif",
    1: "Netral",
    2: "Negatif"
}

# predict sentimen
def predict_sentiment(text, tokenizer, model):
    if tokenizer is None or model is None:
        return "Error", 0.0
    
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )
    with torch.no_grad():
        outputs = model(**inputs)
        probs = softmax(outputs.logits, dim=1)
    pred = torch.argmax(probs, dim=1).item()
    confidence = probs[0][pred].item()
    return label_map_sentimen[pred], confidence