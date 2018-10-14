# Mr. Worldide

Our project for the 2018 edition of McHacks

## Inspiration  

When travelling in a new place, it is often the case that one doesn't have an adequate amount of mobile data to search for information they need.

## What it does

Mr.Worldwide allows the user to send queries and receive responses regarding the weather, directions, news and translations in the form of sms and therefore without the need of any data.

## How we  built it

A natural language understanding model was built and trained with the use of Rasa nlu. This model has been trained to work as best possible with many variations of query styles to act as a chatbot. The queries are sent up to a server by sms with the twill API. A response is then sent back the same way to function as a chatbot.
