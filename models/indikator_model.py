# INDIKATOR SOURCE MODEL
import torch
import pickle
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax

# load indikator hasil best model
@st.cache_resource
def load_indikator_model():
    try:
        path = "indikator_best_model"
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForSequenceClassification.from_pretrained(path)
        model.eval()
        return tokenizer, model
    except Exception as e:
        st.error(f"Gagal memuat model indikator: {e}")
        return None, None

# load indikator label mapping
@st.cache_resource
def load_indikator_labels():
    try:
        with open('id2indikator.pkl', 'rb') as f:
            id2indikator = pickle.load(f)
        indikator_labels_list = [id2indikator[i] for i in sorted(id2indikator.keys())]
        label_map_indikator = {i: label for i, label in enumerate(indikator_labels_list)}
        return label_map_indikator
    except Exception as e:
        st.error(f"Gagal memuat mapping label indikator: {e}")
        return None

# predict indikator
def predict_indikator(text, tokenizer, model, label_map):
    if tokenizer is None or model is None or label_map is None:
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
    return label_map[pred], confidence