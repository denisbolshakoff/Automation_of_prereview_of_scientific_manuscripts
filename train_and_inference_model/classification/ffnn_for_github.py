# Работа с Google Drive в Colab
from google.colab import drive

# Регулярные выражения для поиска и обработки текста
import re

# Численные вычисления и массивы
import numpy as np

# Работа с zip-архивами
from zipfile import ZipFile


# Очистка текстов и лемматизация
!pip install pymorphy3
import pymorphy3
from pymorphy3 import MorphAnalyzer
# pymorphy3 — морфологический анализ русского языка

# NLTK — инструменты для обработки естественного языка
import nltk
import string

from nltk import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt_tab') # Таблицы для токенизации
nltk.download('punkt')     # Токенизация текста
nltk.download('stopwords') # Стоп-слова для разных языков
stopwords_ru = stopwords.words('russian') # Русские стоп-слова

morph = MorphAnalyzer() # Инициализация морфологического анализатора

# Сохранение и загрузка объектов Python
import pickle

# Работа с табличными данными
import pandas as pd
import numpy as np

# Разделение данных на обучающую и тестовую выборки
from sklearn.model_selection import train_test_split

# Метрики для оценки качества классификации
from sklearn.metrics import classification_report, accuracy_score

# Генерация случайных чисел
import random

# PyTorch — фреймворк для глубокого обучения
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# Подсчёт частот элементов
from collections import Counter

# Функция softmax для вероятностной интерпретации выходов модели
from torch.nn.functional import softmax

# Функция для преобразования текста в вектор
def get_text_vector(tokens):
    token_indexes = [indexes.get(token) for token in tokens]
    tensor = torch.zeros(len(vocabulary))
    for i in token_indexes:
        if i is not None:
            tensor[i] = 1
    return tensor.unsqueeze(0)

# Объявляем класс с полносвязной нейронной сетью
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


# Процедуры извлечения данных из архива и чтения имён файлов
def texts_from_zip(path_to_archive):
    texts = []
    with ZipFile(path_to_archive) as zip_archive:
        for name in zip_archive.namelist():
            if '.txt' in name:
                text = zip_archive.read(name)
                text = text.decode('utf-8')
                texts.append(text)
    return texts

def get_filenames(path_to_archive):

    names = []

    with ZipFile(path_to_archive) as zip_archive:
        for name in zip_archive.namelist():
            #print(name)
            if '.txt' in name:
              # перекодирование в читаемую Google Collab'ом кодировку
                names.append(name.encode('cp437').decode('cp866').split('/')[0])
    return names


def clearing_text(article, only_noun = False):

#    clean_texts = []

    article = re.sub(r'Поступила.*\n','',article)

    article = re.sub(r'Для цитирования.*\n','',article)

    article = re.sub(r'Ключевые слова.*\n','',article)

  # приводим к нижнему индексу
    article =  article.lower()

  # убираем УДК
    article = re.sub(r'удк.*\n','',article)

  # убираем перевод строки
    article = re.sub(r'\n',' ',article)

  # убираем табуляцию
    article = re.sub(r'\t',' ',article)

  # убираем ссылку на рисунки
    article = re.sub(r'рис.\s{0,1}[0-9]{1,2}',' ',article)

  #Убираем отдельно стоящее число
    article = re.sub(r'\s[0-9]\s',' ',article)

  #Убираем  ссылки на формулы
    article = re.sub(r'\([0-9]{1,2}\)',' ',article)

  # убираем ссылки на литературу
    article = re.sub(r'\[[0-9А-Яа-я-\,\. ]+\]','',article)

  # убираем нумерацию
    article = re.sub(r'[0-9]{1,2}\.','',article)

  # Заменяем всё от начала слов "Список литературы до конца", тем самым убираем и список литературы и сведения об авторах
    article = re.sub(r'список литературы.*','',article)

  # удаляем спец символы
    article = re.sub(r'\uf0e3',' ',article) # спец символ
    article = re.sub(r'\uf02d','–',article) # спец символ тире
    article = re.sub(r'\xa0',' ',article) # спец символ неразрывный пробел
    #article = re.sub(r'-',' ',article) # символ дефис

  # на всякий случай в конце удаляем всё, что не русские буквы
    article = re.sub('[^а-яА-ЯёЁ -]', '', article)

  # проверяем нужны ли все части речи или только существительные
    if not only_noun:
      # все части речи
      lemmatized_text = [morph.parse(tok)[0].normal_form for tok in word_tokenize(article)]
    else:
      # только существительные
      lemmatized_text = [morph.parse(tok)[0].normal_form for tok in word_tokenize(article)
        if str(morph.parse(tok)[0][1]).split(',')[0].split()[0]=="NOUN"]
   # убираем стоп слова из текста и объединяем лемматизированные слова в текст через пробел
    text_no_stop = ' '.join([token for token in lemmatized_text if token not in stopwords_ru])
    return text_no_stop

# Импортируем библиотеку drive для обеспечения доступа к исходным данным
drive.mount('/content/drive')

# читаем архив статей из zip диска Google Drive
path_to_archive = '/content/drive/MyDrive/articles_6.zip'

# Создаем массивы текстов и имен файлов
names = get_filenames(path_to_archive)

texts = texts_from_zip(path_to_archive)

# Создаем массив для будущего обучения и визуализации из меток опубликованных и неопубликованных статей
published_color = []

for i in names:
  # если статья опубликована - то есть признак "П" - принята, то красим в цвет "0"
  if len(re.findall('О',i))!=0:
    published_color.append(0)
  # если статья неопубликована (других вариантов не остается), то есть признак "О" - отказ, красим в цвет "1"
  else:
    published_color.append(1)



###################### Либо обрабатываем всё снова
# обрабатываем корпус текстов регулярными выражениями
#clean_texts = [clearing_text(text) for text in tqdm(texts)]
# Сохраняем обработанные тексты
#with open('clean_texts_articles_6.pkl', 'wb') as f:
#    pickle.dump(clean_texts, f)



###################### Либо загружаем обработанный
#Загружаем сохранённые тексты обратно
with open('/content/drive/MyDrive/clean_texts_articles_6.pkl', 'rb') as f:
    clean_texts = pickle.load(f)

# Построение DataFrame
df = pd.DataFrame(np.column_stack([clean_texts, published_color]), columns=['Text', 'Label'])

# Метки статей
LABELS = {'0': 0, '1': 1}

vocabulary = set()
lemmatized_texts = []
encoded_labels = []

for _, row in df.iterrows():
    text = row['Text'].split()
    lemmas = []

    # Добавляем токены в набор лексем
    for token in text:
        lemmas.append(token)
        vocabulary.add(token)

    # Кодируем метки
    encoded_labels.append(torch.tensor([LABELS[str(row['Label'])]], dtype=torch.long))
    lemmatized_texts.append(lemmas)

# Конвертируем лексемы в сортированный список
vocabulary = sorted(list(vocabulary))

# Создание индекса лексем
indexes = {word: idx for idx, word in enumerate(vocabulary)}



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
input_dim = len(vocabulary)
hidden_dim = 128
output_dim = len(LABELS)  # 2 возможных значения: 0 и 1
model = FFNN(input_dim, hidden_dim, output_dim).to(device)
criterion = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 4
losses = []

for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    correct_predictions = 0
    for text, label in zip(lemmatized_texts, encoded_labels):
        optimizer.zero_grad()
        inputs = get_text_vector(text).to(device)
        outputs = model(inputs)
        labels = label.to(device)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        predicted_class = torch.argmax(outputs, dim=1)
        correct_predictions += (predicted_class == labels).sum().item()

    avg_loss = total_loss / len(lemmatized_texts)
    losses.append(avg_loss)
    accuracy = correct_predictions / len(lemmatized_texts)
    print(f"Эпоха {epoch + 1}, Потеря: {avg_loss:.4f}, Точность: {accuracy * 100:.2f}%")

# Финальная проверка на новых данных
'''
line_tensor = get_text_vector(clearing_text(text_new_1).split())
outputs = model(line_tensor.to(device))
prediction = torch.argmax(outputs, dim=1)[0].item()
print(f"Предсказанная метка нового текста: {prediction}")
'''

# Сохраняем модель и её состояние
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': losses[-1],
    'vocabulary': vocabulary,
    'labels': LABELS
}, 'model_checkpoint.pth')

text_new_6='''
Текст-болванка по радиотехнике
Введение
В современных автоматизированных системах обработки информации (АСОИ) ключевую роль играет эффективная визуализация технических данных на картографическом интерфейсе. Быстрая интерпретация и анализ информации человеком-оператором (ЧО) становятся критичными для принятия оперативных решений. В данной работе рассматривается задача оптимизации времени восприятия информации с помощью структурного анализа картографического интерфейса и выбора визуальных переменных.

Структурный анализ картографического интерфейса
Картографический интерфейс (КИ) служит интерактивным средством отображения географической информации и технических показателей, поступающих с удалённых объектов. Для повышения эффективности работы оператора необходимо разработать информационную модель, учитывающую свойства визуальных переменных: позиция, форма, ориентация, цвет, текстура, значение и размер. Эти параметры позволяют структурировать данные и обеспечить их быстрое восприятие.

Свойства восприятия визуальных переменных
В работе выделены основные свойства восприятия визуальных переменных: ассоциативность, селективность, упорядоченность и количественность. Для каждой переменной определено, какие из этих свойств применимы. Например, позиция и форма обладают ассоциативностью, а размер — количественностью. Правильный выбор сочетания переменных и их свойств позволяет минимизировать время анализа информации.

Экспериментальный анализ
Для подтверждения эффективности предложенного подхода был проведён эксперимент с участием операторов, не имеющих специальных технических навыков. Сравнивались интерфейсы с различным набором визуальных переменных. Результаты показали, что при использовании оптимальных переменных время восприятия информации сократилось на 50% при сохранении высокого уровня правильных ответов.

Вывод
Проведённые исследования подтверждают, что структурный анализ картографического интерфейса, грамотный выбор визуальных переменных и их свойств позволяют существенно повысить эффективность работы автоматизированных систем обработки информации. Оптимизация восприятия технических данных способствует ускорению принятия решений и повышению качества анализа.
'''

# Загружаем модель и словарь
checkpoint = torch.load('model_checkpoint.pth')
vocabulary = checkpoint['vocabulary']
LABELS = checkpoint['labels']

# Создание индекса лексем
indexes = {word: idx for idx, word in enumerate(vocabulary)}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Восстанавливаем состояние модели
model = FFNN(len(vocabulary), 128, len(LABELS)).to(device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Обработка нового текста
#text_input = args.text
tokens = clearing_text(text_new_6).split()
inputs = get_text_vector(tokens).to(device)

# Прогон инференса
outputs = model(inputs)
prediction = torch.argmax(outputs, dim=1)[0].item()
label = list(LABELS.keys())[list(LABELS.values()).index(prediction)]

probs = torch.exp(outputs)[0][1].item()

print(f"Вероятность публикации: {round(probs,3)}")