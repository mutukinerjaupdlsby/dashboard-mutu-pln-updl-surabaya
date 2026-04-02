# KELUHAN SOURCE MODEL
import torch
import pickle
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
from utils.config import INDIKATOR_KELUHAN_MAP

# load keluhan hasil best model
@st.cache_resource
def load_keluhan_model():
    try:
        path = "keluhan_best_model"
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForSequenceClassification.from_pretrained(path)
        model.eval()
        return tokenizer, model
    except Exception as e:
        st.error(f"Gagal memuat model keluhan: {e}")
        return None, None

# load keluhan label mapping
@st.cache_resource
def load_keluhan_labels():
    try:
        with open('id2keluhan.pkl', 'rb') as f:
            id2keluhan = pickle.load(f)
        keluhan_labels_list = [id2keluhan[i] for i in sorted(id2keluhan.keys())]
        label_map_keluhan = {i: label for i, label in enumerate(keluhan_labels_list)}
        return label_map_keluhan
    except Exception as e:
        st.error(f"Gagal memuat mapping label keluhan: {e}")
        return None

# predict keluhan
def predict_keluhan(text, tokenizer, model, label_map):
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

# Validate keluhan based on indikator mapping
def validate_keluhan_with_indikator(indikator, keluhan):
    if indikator in INDIKATOR_KELUHAN_MAP:
        allowed_keluhan = INDIKATOR_KELUHAN_MAP[indikator]
        if keluhan not in allowed_keluhan:
            return allowed_keluhan[0] if allowed_keluhan else keluhan
    return keluhan