# People-also-ask Api

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![PyPI](https://img.shields.io/pypi/v/people_also_ask.svg)](https://pypi.org/project/people-also-ask)
[![versions](https://img.shields.io/pypi/pyversions/people_also_ask.svg)](https://github.com/lagranges/people_also_ask)

People-also-ask provides APIs to easily crawl the data of google featured snippet.

## ⚠ Warning
Search engines like Google do not allow any sort of automated access to their service but from a legal point of view there is no known case or broken law. Google does not take legal action against scraping, likely for self-protective reasons.
API have been configured to not abuse google search engine.

## Installation
```
pip install people_also_ask 
```

## Usage
Goal of ``people_also_ask`` is to provide simple and easy to use API for retrieving informations from Google Featured Snippet.

### Importing
```python
import people_also_ask
```

### How to get related questions 
```python
people_also_ask.get_related_questions("coffee")

['Is coffee good for your health?',
 	'Why is coffee bad for you?',
 	'Who invented coffee?',
	'What do u know about coffee?']
```

### How to get more questions
```python
people_also_ask.get_related_questions("coffee", 5)

['How did coffee originate?',
	'Is coffee good for your health?',
  'Who brought coffee America?',
	'Who invented coffee?',
	'Why is coffee bad for you?',
	'Why is drinking coffee bad for you?']
```

### Generate unlimited questions
```python
for question in people_also_ask.generate_related_questions("cofee")

Why is coffee bad for you?
Who invented coffee?
Is coffee good for your health?
Who brought coffee America?
How did coffee originate?
Why is drinking coffee bad for you?
....
```

### Get answer for a question
```python
people_also_ask.get_answer("Why is coffee bad for you?")

{'has_answer': True,
 'question': 'Why is coffee bad for you?',
 'related_questions': ['Why is drinking coffee bad for you?',
  'Is coffee good for your health?',
  'Is coffee toxic to your body?',
  'What does coffee do to your body?'],
 'response': 'Consuming too much caffeine can lead to jitteriness, anxiety, heart palpitations and even exacerbated panic attacks (34). If you are sensitive to caffeine and tend to become overstimulated, you may want to avoid coffee altogether. Another unwanted side effect is that it can disrupt sleep ( 35 ).Aug 30, 2018',
 'heading': 'Consuming too much caffeine can lead to jitteriness, anxiety, heart palpitations and even exacerbated panic attacks (34). If you are sensitive to caffeine and tend to become overstimulated, you may want to avoid coffee altogether. Another unwanted side effect is that it can disrupt sleep ( 35 ).Aug 30, 2018',
 'title': 'Coffee — Good or Bad? - Healthline',
 'link': 'https://www.healthline.com/nutrition/coffee-good-or-bad#:~:text=Consuming%20too%20much%20caffeine%20can,can%20disrupt%20sleep%20(%2035%20).',
 'displayed_link': 'www.healthline.com › nutrition › coffee-good-or-bad',
 'snippet_str': 'Consuming too much caffeine can lead to jitteriness, anxiety, heart palpitations and even exacerbated panic attacks (34). If you are sensitive to caffeine and tend to become overstimulated, you may want to avoid coffee altogether. Another unwanted side effect is that it can disrupt sleep ( 35 ).Aug 30, 2018\nwww.healthline.com › nutrition › coffee-good-or-bad\nhttps://www.healthline.com/nutrition/coffee-good-or-bad#:~:text=Consuming%20too%20much%20caffeine%20can,can%20disrupt%20sleep%20(%2035%20).\nCoffee — Good or Bad? - Healthline',
 'snippet_data': None,
 'date': None,
 'snippet_type': 'Definition Featured Snippet',
 'snippet_str_body': '',
 'raw_text': 'Featured snippet from the web\nConsuming too much caffeine can lead to jitteriness, anxiety, heart palpitations and even exacerbated panic attacks (34). If \nyou\n are sensitive to caffeine and tend to become overstimulated, \n may want to avoid \ncoffee\n altogether. Another unwanted side effect is that it can disrupt sleep ( 35 ).\nAug 30, 2018\nCoffee — Good or Bad? - Healthline\nwww.healthline.com\n › nutrition › coffee-good-or-bad'}
```

### Get Simple Answer for a question
```python
people_also_ask.get_simple_answer("Why is coffee bad for you?")

'Consuming too much caffeine can lead to jitteriness, anxiety, heart palpitations and even exacerbated panic attacks (34). If you are sensitive to caffeine and tend to become overstimulated, you may want to avoid coffee altogether. Another unwanted side effect is that it can disrupt sleep ( 35 ).Aug 30, 2018'
```


### Generate questions and answers relative to a subject
```python
people_also_ask.generate_answer("coffee")
```


### Using proxies

```python
import people_also_ask.request.session

people_also_ask.request.session.set_proxies(
    (
        "http://1234.5.6.7:8080",
        "http://1237.5.6.7:8080",
    )
)
```