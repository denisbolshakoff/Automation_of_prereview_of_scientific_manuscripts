---

## Description languages

This README is available in two languages:
- Russian version below 🇷🇺
- English version follows 🇬🇧

---

# Автоматизация предрецензирования научных рукописей

## Описание
В докладе представлены результаты применения больших языковых моделей (LLM) на архитектуре трансформеров для оптимизации редакционно-издательского процесса на этапе подготовки научных рукописей к рецензированию. Рассматриваются три направления предварительной обработки материалов.
1.​Предварительная оценка перспективы публикации. Для анализа текста рукописи и прогнозирования вероятности её принятия к публикации использованы трансформерные модели, в том числе BERT и Longformer. Модели обучались на корпусе ранее рассмотренных материалов и позволяли отнести новую рукопись к категории «принята» или «отклонена». Апробация метода проведена на материалах научно-технического журнала «Вестник Концерна ВКО „Алмаз – Антей“». На корпусе из 1000 рукописей с равным распределением принятых и отклонённых статей достигнута доля правильных ответов около 90%.

2.​Подбор рецензента(ов). Для назначения рецензента формируется векторное представление текста рукописи (числовое описание её содержания), после чего оно сопоставляется с представлениями ранее рецензированных работ с использованием косинусного сходства. Такой подход позволяет определить экспертов, уже работавших с близкой тематикой, и повысить обоснованность распределения рукописей. В случае, если по результатам предварительной оценки публикационная перспектива признана низкой, целесообразно назначение только одного рецензента для подготовки мотивированного отказа.

3.​Автоматическая генерация краткого резюме. Для создания сжатого описания содержания статьи применяется трансформерная модель, способная формировать связное резюме объёмом 4–5 предложений на основе полного текста рукописи. Подготовленное резюме используется для предварительного ознакомления рецензента с тематикой и вкладом работы, что сокращает время принятия решения о согласии на рецензирование.

Внедрение предложенного подхода позволяет сократить среднее время, затрачиваемое экспертами на рецензирование, примерно на 15% без изменения стандартов научной оценки.

## Лицензия
![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)

Этот проект распространяется под лицензией [CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/) (Creative Commons Attribution-NonCommercial).

## Цели проекта
В процессе написания...

## Задачи проекта
В процессе написания...


## "Инструменты" проекта
В процессе написания...

## Интересный результат
В процессе написания...

## Результаты проекта
В процессе написания...


> [!IMPORTANT] 
> Тексты рукописей были взяты из научно-технического журнала Вестник Концерна ВКО "Алмаз - Антей" (с 2011 по 2024 годы). Опубликованные тексты можно найти в интернете, не опубликованные нет.


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
In process...


## Key Findings
In process...

> [!IMPORTANT]
> The texts were sourced from the Scientific Journal of "Almaz - Antey" Air & Space Defense Corporation (covering publications from 2011–2024). Published materials are accessible online, while unpublished ones remain confidential.