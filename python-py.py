from flask import Flask, render_template, request, jsonify, flash
import os
import random
from werkzeug.utils import secure_filename

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from collections import Counter
from torch.nn.functional import softmax
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


import pandas as pd
import numpy as np
from zipfile import ZipFile

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import random

import pickle

import pymorphy3
from pymorphy3 import MorphAnalyzer

import nltk
import string
import re

from nltk import word_tokenize
from nltk.corpus import stopwords

import threading
import uuid

tasks = {}


nltk.download('punkt_tab')
#nltk.download('punkt')
#nltk.download('stopwords')
stopwords_ru = stopwords.words('russian')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

print("Loading models...")

device = "cpu"

# -------------------------
# Morphology
# -------------------------
morph = MorphAnalyzer()

# -------------------------
# T5 MODEL
# -------------------------
MODEL_DIRECTORY = "./absum"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_DIRECTORY,
    local_files_only=True,
    trust_remote_code=True,
    use_fast=False
)


t5_model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_DIRECTORY,
    local_files_only=True
).to(device)

t5_model.eval()

# -------------------------
# CLASSIFICATION MODEL
# -------------------------
checkpoint_file = 'model_checkpoint.pth'

checkpoint = torch.load(checkpoint_file, map_location=torch.device('cpu'))
print("чекпоинт загружен")
vocabulary = checkpoint['vocabulary']
print("словарь загружен")
LABELS = checkpoint['labels']
print("метки загружены")

class FFNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.log_softmax = nn.LogSoftmax(dim=-1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return self.log_softmax(x)

classifier_model = FFNN(len(vocabulary), 128, len(LABELS))
classifier_model.load_state_dict(checkpoint['model_state_dict'])
classifier_model.eval()

# словарь индексов
indexes = {word: idx for idx, word in enumerate(vocabulary)}

print("Models loaded.")



app.secret_key = 'your-secret-key-here'  # необходим для flash-сообщений

# Ограничения для загрузки файлов
ALLOWED_EXTENSIONS = {'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 МБ


df__11 = pd.read_excel('1_6.xlsx', header=None)

with open('clean_texts_articles_6.pkl','rb') as f:
    clean_texts = pickle.load(f)


def published(article_input):

   # Функция для преобразования текста в вектор
    def get_text_vector(tokens):
        token_indexes = [indexes.get(token) for token in tokens]
        tensor = torch.zeros(len(vocabulary))
        for i in token_indexes:
            if i is not None:
                tensor[i] = 1
        return tensor.unsqueeze(0)
    
    # Обработка нового текста
    #text_input = args.text
    tokens = clearing_text(article_input).split()
    inputs = get_text_vector(tokens).to(device)

    # Прогон инференса
    with torch.no_grad():
        outputs = classifier_model(inputs)
        probs = torch.exp(outputs)
    
    publish_prob = probs[0][1].item()
    reject_prob = probs[0][0].item()


    prediction = torch.argmax(outputs, dim=1)[0].item()
    label = list(LABELS.keys())[list(LABELS.values()).index(prediction)]
    
    if publish_prob > reject_prob:
        decision = '🟢 будет опубликована '
    else:
        decision = '🔴 будет отклонена '

    return '{} (вероятность публикации {:.3f})'.format(decision, publish_prob)



def T5paraphrase(article_input):
    MODEL_DIRECTORY = "./absum" 

    try:
        if not os.path.isdir(MODEL_DIRECTORY):
            raise FileNotFoundError(f"Папка {MODEL_DIRECTORY} не найдена.")
        
        # Проверяем наличие ключевых файлов (необязательно, но полезно)
        required_files = ['config.json', 'tokenizer_config.json']
        for file in required_files:
            if not os.path.exists(os.path.join(MODEL_DIRECTORY, file)):
                return f"Предупреждение: в папке нет файла {file}. Загрузка может не сработать."
            else:
                print(file)
        
        print("Загружаем модель на CPU...")
        
    except Exception as e:
        print(f"✗ Произошла ошибка: {str(e)}")
    device="cpu"



    # -------------------------
    # Разбиение на куски
    # -------------------------

    def chunk_text(text, max_tokens=100):
        tokens = tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk = tokens[i:i + max_tokens]
            chunks.append(tokenizer.decode(chunk))
        return chunks


    # -------------------------
    # Генерация summary
    # -------------------------

    def generate_summary(text, max_new_tokens=200):
        #inputs = tokenizer(f'Резюме статьи:\n\n{text}', return_tensors="pt").to("cpu")
        inputs = tokenizer(
            f'Резюме статьи:\n\n{text}',
            return_tensors="pt"
        ).to(device)
        with torch.no_grad():
            outputs = t5_model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                num_beams=4,
                temperature=0.7,  # Немного увеличил для разнообразия
                top_k=50,
                top_p=0.95,
                early_stopping=False,
                no_repeat_ngram_size=3,  # Избегаем повторений
                length_penalty=1.5  # Поощряем более длинные последовательности (>1)
            )

        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result.strip()
  
    # -------------------------
    # Основной pipeline
    # -------------------------
    #print(article_input[:500])
    chunks = chunk_text(article_input[200:700])

    #partial_summaries = [generate_summary(chunk, max_new_tokens=10) for chunk in chunks]  # Увеличьте значение
    #print(chunks)
    print(" ".join(chunks))
    final_summary = generate_summary(" ".join(chunks), max_new_tokens=50)  # Увеличьте значение
    #final_summary = generate_summary(" ".join(chunks[:100]), max_new_tokens=5)

    return final_summary


# Логика подготовки текста
def clearing_text(article, only_noun=False):

    article = re.sub(r'Поступила.*\n', '', article)
    article = re.sub(r'Для цитирования.*\n', '', article)
    article = re.sub(r'Ключевые слова.*\n', '', article)
    article = article.lower()
    article = re.sub(r'удк.*\n', '', article)
    article = re.sub(r'\n', ' ', article)
    article = re.sub(r'\t', ' ', article)
    article = re.sub(r'рис.\s{0,1}[0-9]{1,2}', ' ', article)
    article = re.sub(r'\s[0-9]\s', ' ', article)
    article = re.sub(r'$[0-9]{1,2}$', ' ', article)
    article = re.sub(r'$$[0-9А-Яа-я-\,\. ]+$$', '', article)
    article = re.sub(r'[0-9]{1,2}\.', '', article)
    article = re.sub(r'список литературы.*', '', article)
    article = re.sub(r'\uf0e3', ' ', article)
    article = re.sub(r'\uf02d', '–', article)
    article = re.sub(r'\xa0', ' ', article)
    article = re.sub('[^а-яА-ЯёЁ -]', '', article)

    if not only_noun:
        lemmatized_text = [morph.parse(tok)[0].normal_form for tok in word_tokenize(article)]
    else:
        lemmatized_text = [
            morph.parse(tok)[0].normal_form
            for tok in word_tokenize(article)
            if str(morph.parse(tok)[0][1]).split(',')[0].split()[0] == "NOUN"
        ]

    text_no_stop = ' '.join(token for token in lemmatized_text if token not in stopwords_ru)
    return text_no_stop

# Функция для сравнения текстов
def reviewer(new_article_1):
    #df__11 = pd.read_excel('1_6.xlsx', header=None)

    #with open('clean_texts_articles_6.pkl', 'rb') as f:
    #   clean_texts = pickle.load(f)

    new_article = clearing_text(new_article_1)
    vectorizer = CountVectorizer()
    all_articles = clean_texts + [new_article]
    vectors = vectorizer.fit_transform(all_articles)
    existing_vectors = vectors[:-1].toarray()
    new_vector = vectors[-1].toarray().reshape(1, -1)
    similarities = cosine_similarity(new_vector, existing_vectors)[0]
    best_match_idx = np.argmax(similarities)
    return df__11.loc[best_match_idx][4]


# Главная страница
@app.route('/', methods=['GET'])
def home():
    return render_template(
        'index.html',
        title='Предрецензирование научных рукописей',
        message='Загрузите txt-файл рукописи в модель...',
        second_message='<пусто>',
        third_message='<пусто>',
        fourth_message='<пусто>'
    )

@app.route('/process', methods=['POST'])
def process():

    if 'file' not in request.files:
        return jsonify({"error": "file missing"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "only txt allowed"}), 400

    content = file.stream.read().decode('utf-8')

    task_id = str(uuid.uuid4())

    tasks[task_id] = {
        "status": "starting",
        "second_message": "",
        "third_message": "",
        "fourth_message": ""
    }

    thread = threading.Thread(target=process_article, args=(task_id, content))
    thread.start()

    return jsonify({"task_id": task_id})


@app.route('/status/<task_id>')
def status(task_id):

    task = tasks.get(task_id)

    if not task:
        return jsonify({"error": "task not found"}), 404

    return jsonify(task)

# Проверка разрешения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_article(task_id, content):

    tasks[task_id]["status"] = "processing"

    # 1. классификация
    published_result = published(content)
    tasks[task_id]["second_message"] = published_result

    # 2. подбор рецензента
    review_result = reviewer(content)
    tasks[task_id]["third_message"] = review_result

    # 3. суммаризация (самая долгая)
    paraphrase = T5paraphrase(content)
    tasks[task_id]["fourth_message"] = paraphrase

    tasks[task_id]["status"] = "done"


# Запуск приложения
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)