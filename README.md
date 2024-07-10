# cpi-forecast-service

This is a web app that uses ML to forecast Consumer Prices Indicies (CPI)

- This work states that best performance (lowest RMCE) for forecasting CPI data is shown by Elastic Net model (p5.1)
- https://www.bis.org/ifc/publ/ifcb57_18.pdf

- Using seasonal adjustments lower RMSE estimated by ~10% (p5.4)

# TODO

- [x] Доработать все кнопочки
    - [x] Загрузка данных вручную
    - [x] Скачка образца данных
- [x] Создавать все нужные директории при запуске проекта
- [ ] Оценка доверительного интервала в метаданных
- [ ] Превратить алерт "модели удалены" в flash
- [ ] Добавить ориентировочное время загрузки
- [ ] NotImplemented error
- [ ] Удалить старый _get_data
- [ ] Добавить кеширование запросов для получения метадаты и графичков
- [ ] Фиксануть верстку странички индекс
- [ ] Почистить зависимости
- [ ] Запаролить
- [ ] Задеплоить на сервере, настроить actions
- [ ] Распаролить, сдать

## Техническое задание для тестовой задачи

### Общее описание задачи

Разработать программное решение, которое будет автоматически скачивать или загружать с помощью пользователя данные по
индексам потребительских цен с официального сайта Госкомстата, анализировать полученные данные, строить модель прогноза
на 6 месяцев вперед и представлять результаты в виде графика на веб-сайте. Весь код должен быть упакован в
Docker-контейнер и размещен на GitHub для оценки.

### Технические требования

#### Инструменты и технологии

Язык программирования: Python 3.9
Фреймворк для веб-разработки: Flask
Библиотеки для анализа данных: pandas, numpy
Библиотеки для построения моделей: scikit-learn, statsmodels
Виртуализация: Docker
Контроль версий: Git, GitHub

#### Версии библиотек

scikit-learn: 0.24.1
statsmodels: 0.13.1
pandas: 1.3.5
numpy: 1.21.5
flask:  2.0.3

### Функциональные требования, этапы разработки:

1. Сбор данных:
   Разработать скрипт для автоматического скачивания данных по индексам потребительских цен с сайта Госкомстата.
   Данные могут быть обогащены дпольнительными источниками, что является плюсом для проекта.

#### Результат: скрипт для скачки данных ./services/download_data.py

2. Анализ и обработка данных:
   Провести предварительный анализ и очистку данных.
   Подготовить данные для построения прогнозной модели.

#### Результат: скрипт для очистки и подготовки данных ./services/clean_data.py

3. Построение модели прогноза:
   Использовать подходящие алгоритмы машинного обучения для построения модели прогноза индексов потребительских цен на 6
   месяцев вперед.
   Оценить точность и надежность построенной модели.

#### Результат: скрипт для построения моделей ./services/auto_process_data.py

4. Разработка веб-сайта презентации:
   Создать простой веб-сайт на Flask, состоящий из 1-2 страниц.
   На сайте должна быть возможность загрузки (форма) либо отображения загрузки актуальных данных и отображения графика
   прогноза модели.

5. Docker и GitHub:
   Весь проект должен быть упакован в Docker-контейнер для обеспечения легкости развертывания и портативности.
   Исходный код проекта должен быть размещен на GitHub в открытом доступе вместе с Dockerfile.

### Нефункциональные требования

- Проект должен быть легко развертываемым на любой системе с предустановленным Docker.
- Код должен быть чистым, хорошо структурированным и документированным.
- Интерфейс веб-сайта должен быть простым и понятным для пользователя.
- Не требуется сверхточная модель, но модель, выдающий адекватный прогноз будет вашим преимуществом.
- Интерпретируемость факторов модели не требуется.
- Вероятностная оценка доверительного интервала на график прогноза будет вашим преимуществом.

### Сдача проекта

- Весь исходный код должен быть загружен в репозиторий на GitHub.
- В репозитории должен быть файл README.md с инструкциями по развертыванию и использованию проекта.
- Должна быть предоставлена ссылка на репозиторий для оценки.
- Версии библиотек должны соответствовать, указанным в задании, при необходимости допускаются 1-2 дополнительные
  библиотеки, необходимые для проекта.

### Сроки выполнения

- Проект должен быть выполнен и представлен для проверки в течение 1 недели с момента получения задания.