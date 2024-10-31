import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from underthesea import word_tokenize
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

class FoodAIModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = MultinomialNB()
        self.intent_labels = ['món_ăn', 'công_thức', 'đặt_bàn', 'giá_cả', 'khác']
        
        # Load dữ liệu từ database
        self.food_data = self._load_food_data()
        
    def _load_food_data(self):
        """Load dữ liệu từ JSON file"""
        try:
            with open('data/vietnam_food_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def preprocess_text(self, text):
        """Tiền xử lý văn bản tiếng Việt"""
        # Tách từ using underthesea
        words = word_tokenize(text.lower())
        return ' '.join(words)

    def train(self, training_data):
        """Training model với dữ liệu mới"""
        X = [self.preprocess_text(item['text']) for item in training_data]
        y = [item['intent'] for item in training_data]
        
        # Vectorize text
        X_vectorized = self.vectorizer.fit_transform(X)
        
        # Train classifier
        self.classifier.fit(X_vectorized, y)
        
        # Save model
        self._save_model()

    def predict_intent(self, text):
        """Dự đoán intent của câu hỏi"""
        preprocessed = self.preprocess_text(text)
        vectorized = self.vectorizer.transform([preprocessed])
        intent = self.classifier.predict(vectorized)[0]
        return intent

    def find_best_match(self, query, threshold=0.5):
        """Tìm món ăn phù hợp nhất với câu hỏi"""
        best_match = None
        best_score = 0
        
        query_vector = self.vectorizer.transform([self.preprocess_text(query)])
        
        for food in self.food_data:
            food_text = f"{food['name_vi']} {food['description_vi']}"
            food_vector = self.vectorizer.transform([self.preprocess_text(food_text)])
            
            similarity = (query_vector * food_vector.T).toarray()[0][0]
            
            if similarity > best_score and similarity > threshold:
                best_score = similarity
                best_match = food
                
        return best_match, best_score

    def _save_model(self):
        """Lưu model"""
        with open('models/food_ai_model.pkl', 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'classifier': self.classifier
            }, f)

    def _load_model(self):
        """Load model đã training"""
        try:
            with open('models/food_ai_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
                self.vectorizer = model_data['vectorizer']
                self.classifier = model_data['classifier']
        except FileNotFoundError:
            print("Chưa có model, cần training trước!") 