---

## Description languages

This README is available in two languages:
- Russian version below 🇷🇺
- English version follows 🇬🇧

---

# Автоматизация предрецензирования научных рукописей

## Описание

> [!IMPORTANT]
> Это "обёртка" (*frontend*) над языковыми моделями, которая не будет работать при загрузке на компьютер. 
> По этическим соображениям в репозиторий не загружены:
> - предобученная на архитектуре полносвязных нейронных сетей модель `model_checkpoint.pth`, 
> - файл `1_6.xlsx` с именами рецензентов,
> - предобработанный корпус `clean_texts_articles_6.pkl` опубликованных статей и неопубликованных рукописей.
> 
> *Python*-скрипты для обучения с использованием архитектур полносвязной нейронной сети (*FFNN*), *Bidirectional Encoder Representations from Transformers* (*BERT*) и *Longformer* приведены в репозитории в папке `train_and_inference_model`.

В проекте рассматриваются три направления предварительной обработки текстов для оптимизации редакционно-издательского процесса на этапе подготовки научных рукописей к рецензированию.

1. Предварительная оценка перспективы публикации. Для анализа текста рукописи и прогнозирования вероятности её принятия к публикации использованы трансформерные модели, в том числе *BERT* и *Longformer*. Модели обучались на корпусе ранее рассмотренных материалов и позволяли отнести новую рукопись к категории «принимается» или «отклоняется». Апробация метода проведена на материалах научно-технического журнала «Вестник Концерна ВКО „Алмаз – Антей“». На корпусе из 923 рукописей с примерно равным распределением принятых и отклонённых статей (52 на 48%) достигнута доля правильных ответов около 90% (усредненое значение метрики *accuracy* по ста прогонам лучшей модели – 89,1%).

2. Подбор рецензента(ов). Для назначения рецензента формируется векторное представление текста рукописи (числовое описание её содержания), после чего оно сопоставляется с представлениями ранее рецензированных работ с использованием косинусного сходства. Такой подход позволяет определить экспертов, уже работавших с близкой тематикой, и повысить обоснованность распределения рукописей. В случае, если по результатам предварительной оценки публикационная перспектива признана низкой, целесообразно назначение только одного рецензента для подготовки мотивированного отказа.

3. Автоматическая генерация краткого резюме. Для создания сжатого описания содержания статьи применяется трансформерная модель, способная формировать связное резюме объёмом 4–5 предложений на основе полного текста рукописи. Подготовленное резюме используется для предварительного ознакомления рецензента с тематикой и вкладом работы, что сокращает время принятия решения о согласии на рецензирование.

Внедрение предложенного подхода позволяет сократить среднее время, затрачиваемое экспертами на рецензирование, примерно на 15% без изменения стандартов научной оценки.

<img src="https://raw.githubusercontent.com/denisbolshakoff/Automation_of_prereview_of_scientific_manuscripts/main/screenshot.png" width="250">


## Лицензия
![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)

Этот проект распространяется под лицензией [CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/) (Creative Commons Attribution-NonCommercial).

## Цели проекта
Для вновь приходящей в научный журнал рукописи на основании корпуса опубликованных и неопубликованных текстов определить:
- вероятность опубликования;
- наиболее близкий текст из корпуса;
- краткое резюме.

## Задачи проекта
1. Собрать корпус текстов, рассмотренных рецензентами научно-технического журнала «Вестник Концерна ВКО „Алмаз – Антей“».
2. Предобработать корпус:
	1. Провести очистку от служебных слов (УДК, *DOI*, Список литературы, "Рис." и т. д.)
	2. Удалить стоп-слова
	3. Провести лемматизацию
3. Перевести все тексты корпуса через векторайзеры или эмбеддинги в числовой вид.
4. Применить методы классификации для обучения модели классификации, которая будет применяться к вновь пришедшей рукописи с целью определения вероятности её публикации (или бинарной классификации)
	1. Классические методы машинного обучения (*machine-learning*) или далее *ML*-методы
	2. Методы глубинного обучения (*deep-learning*) или далее *DL*-методы
	3. Трансформеры (*transformers*)
5. Применить методы определения косинусного расстояния с целью определения текста наиболее близкого к поступившей рукописи. Если тексты близки, то на вновь пришедшую статью можно назначить тех же рецензентов, что уже были назначены на статью из корпуса.
6. Сделать парафраз всего текста статьи для получения краткого изложения сути проведенных исследований с целью отправки в электронном письме рецензенту не только полного текста рукописи, но и обозначения с чем придеться работать. По опыту такое резюме чаще приводит к быстрому ответу если рецензент не готов рецензировать рукопись без ознакомления с текстом если тематика ему не близка.
7. Сделать пригодный для использования редакциями научных журналов интерфейс.

## "Инструменты" проекта
- *Python*
- предобученные модели с *HuggingFace*
- *Flask*
- *CSS*
- *HTML*
- *JavaScript*
- *Docker*

## Интересный результат
1. Простая полносвязная нейронная сеть (*FFNN*) с векторайзером `OneHotEncoder` даёт результат в метрике `accuracy` выше, чем та же полносвязная нейронная сеть с более продвинутыми векторайзеры `CountVectorizer`, `TfidfVectorizer` и `HashingVectorizer`. 
2. Аналогичный результат получен при использовании классических методов машинного обучения, а именно использование векторайзера `OneHotEncoder` (`CountVectorizer(binary=True)`) с методом классификации `LogisticRegression` даёт метрику `accuracy` лучше чем у более продвинутых методов вроде градиентного бустинга (`GradientBoostingClassifier`) или случайного леса (`RandomForestClassifier`).

## Описание исходных данных
Для обучения модели использовались текстовые файлы в формате `*.txt` с кодировкой `UTF-8`. В названии файла была введена позиционная и буквенная кодировка

|Название файла|Расшифровка|
|:-|:-|
|0001РП.txt| 0001 - Первый файл, Р - радиолокация, П - принята к публикации|
|0254ГО.txt|0254 - 254 по номеру файл, Г - газодинамика, О - отклонена к публикации|

Используемые для кодировки буквы в пятом символе названия файла:

|Буква|Тематика|
|:-|:-|
|А | Автоматика|
| В | Внешняя тематика|
| Г | Газодинамика|
| Д | обработка Давлением|
| И | Информатика|
| М | Машиностроение|
| Р | Радиолокация|
| Т | Теплофизика|

Используемые для кодировки буквы в шестом символе названия файла
|Буква|Решение|
|:-|:-|
| О | рукопись отклонена к публикации|
| В | рукопись принята к публикации|

## Результаты проекта
Лучшие характеристики:
* по классификации даёт *BERT*-модель, предобученная на большом корпусе научных текстов на русском языке, – `ai-forever/ruSciBERT` ($\mathbb{E}[accuracy]\approx0.89$);
* по определению рецензента путём поиска рукописи, наиболее близкой к вновь пришедшей по косинусному расстоянию, мультифункциональная модель – `BAAI/bge-m3` ($\mathbb{E}[accuracy]\approx0.97$);
* по парафразу дают - семейство моделей *qwen*, но лучше всех показала себя модель  – `Qwen/Qwen2.5-32B-Instruct` (метрика - субъективное восприятие парафраза собственной статьи).

> [!IMPORTANT]
> Для ускорения работы приложения и достижения предельных характеристик *Time to First Token* (*TTFT*) на портативном ноутбуке в коде модели на *github* используются не самые лучшие, но работающие:
> - Предобученная полносвязная нейронная сеть (*FFNN*) с векторайзером *OneHotEncoder* для определения вероятности опубликования (*TTFT* - 1 секунда). Полный инференс модели `ai-forever/ruSciBERT` требует ускорителя не менее *T*4 с 11,8 *GB GPU* и времени инференса менее 1 секунды, однако на *CPU* инференс модели занимает 40 секунд.
> - Модель `CountVectorizer` вместо модели *bge-m3* для определения рецензента (*TTFT* - 2 секунды). Полный инференс модели *bge-m3* на *CPU* достигает 83 часов, а при использовании *G*4 c 90 *GB GPU* - 3 минуты;
> - Модель `cointegrated/rut5-base-absum` c *TTFT* чуть менее 30 секунды при загрузке фрагмента текста от 200 до 700 символов рукописи (не всей рукописи). Лучшая модель для парафраза `Qwen/Qwen2.5-32B-Instruct` требует для инференса 90 *GB GPU * и три минуты машинного времени ускорителя.

> [!IMPORTANT]
> Тексты рукописей были взяты из научно-технического журнала Вестник Концерна ВКО "Алмаз – Антей" (с 2011 по 2024 годы). Опубликованные тексты можно найти в интернете, не опубликованные нет.


# Automation of pre-review of scientific manuscripts

## Description
The repository presents the results of applying large language models (LLMs) based on transformer architectures to optimize the editorial workflow at the stage of preparing scientific manuscripts for peer review. Three directions of preliminary manuscript processing are considered.
1. Preliminary evaluation of publication potential. Transformer-based models, including BERT and Longformer, were used to analyze manuscript texts and predict the probability of acceptance for publication. The models were trained on a corpus of previously processed submissions and classified new manuscripts as either “accepted” or “rejected.” The approach was tested using data from the Journal of “Almaz – Antey” Air and Space Defence Corporation. On a dataset of 1,000 manuscripts with an equal distribution of accepted and rejected papers, the method achieved an accuracy of approximately 90%.

2. Reviewer assignment. A vector representation of each manuscript (a numerical description of its content) is generated and compared with representations of previously reviewed papers using cosine similarity. This method helps identify experts who have already evaluated thematically similar works, thereby improving the consistency and justification of reviewer selection. If the preliminary assessment indicates low publication potential, assigning only a single reviewer to prepare a reasoned rejection is considered sufficient.

3. Automated summary generation. The transformer-based model is applied to generate concise summaries of 4–5 sentences directly from the full manuscript text. These summaries provide reviewers with a structured overview of the study’s topic and contribution, facilitating a faster decision on whether to accept the manuscript for review.

Implementation of the proposed approach reduces the average time required for peer review by approximately 15% while maintaining established standards of scientific evaluation.

## License
![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)

Distributed under the CC BY-NC 4.0 [CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/) (Creative Commons Attribution-NonCommercial).

## Goals of the Project
In process...

## Objectives of the Project
In process...

## Tools Used
In process...

## Notable Result
A simple fully connected neural network with the `OneHotEncoder` vectorizer gives much better results than the `CountVectorizer`, `TfidfVectorizer`, and `HashingVectorizer` vectorizers.

## Key Findings
The best characteristics in terms of classification, cosine distance and paraphrase are given by the following tracer models: *BERT*, *Longformer*, *bge-m3*, *Qwen*.

> [!IMPORTANT]
> The texts were sourced from the Scientific Journal of "Almaz - Antey" Air & Space Defense Corporation (covering publications from 2011–2024). Published materials are accessible online, while unpublished ones remain confidential.
