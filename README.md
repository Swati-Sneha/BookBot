# BookBot

##ChatBot that works on scraped data from https://fbookshelf.herokuapp.com/

This chatbot is meant to serve following use cases: 

  a.List few genres on request
  b.suggest upto three books for asked genre
  c.give the name of the author of the book 
  d.give the url of the book by appending the isbn no. to https:/openlibrary.org/

It also handles other salutations like->greetings(hello, bye and thank you)

###Requirements:
  fuzzywuzzy, nltk
  numpy, random, pickle, 
  nltk.sentiment.vader,  
  nltk.corpus
  
Type bye or its synonyms to exit from the chatbot
