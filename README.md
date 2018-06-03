# Messenger-Weather-Bot
Facebook Weather chatbot using nltk and pyowm weather api provider.
</br>
[Try It !!](https://www.facebook.com/WeatherBot-1544799305629782/)

</br>
</br>



</br>
</br>

## How it works ?

</br>

In this project i didn't use any framework like [Dialogflow](https://dialogflow.com/). The project contains agents that can process the text and recognize entities from it like (time, country, city, places, location....etc), So for the limitation of this task (Weather Forecast) it only extract places and locations entity, then send it to weather agent that contact weather api provider [PyOWM](https://github.com/csparpa/pyowm) for further reading in its documentation [check this out](https://pyowm.readthedocs.io/en/latest/).

The approach of implementing this chatbot is the knowledge based approach in which the agent have knowledge about the question and the answer of the user with some predefined functions and actions accordingly.

</br>

## NLTK

<br>

[NLTK](http://www.nltk.org/) contains over 50 corpus which you can interacts with pretrained models with lexical resources whic you can use friendly in most information extractions tasks. I used nltk ne_chunk pos tags for NER(Named Entity Recognition), although it doesn’t have a proper English corpus for NER. It has the CoNLL 2002 Named Entity CoNLL but it will do pretty good for our task.

</br>

## Deployment

</br>

The backend services of this project is deployed on [Heroku](https://dashboard.heroku.com/)
