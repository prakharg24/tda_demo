# tda_demo

## Installation

Requires Python 3.x and Django. Can be installed simply with the following command

```
python -m pip install Django
```

## Running the Server

1. Change directory to mysite.
```
cd mysite
```
2. Run the following command
```
python manage.py runserver
```
3. Now that the server is running, it can be accessed at [http://localhost:8000/polls/](http://localhost:8000/polls/)

## Relevant Files

1. The figures displayed and the CSS style files are all stored in `mysite/polls/static/polls/`
2. The HTML template files are stored in `mysite/polls/templates/polls/`
3. The HTML parser is present in `views.py`
4. All the signal processing and graph creation happens in `datareader.py`
5. The dataset is present as CSV files in `mysite/polls/dataset/`
