# BookBot

### ChatBot that works on scraped data from https://fbookshelf.herokuapp.com/

The data is scraped from the link using the script ***book_scraper.py*** using beautiful-soup library. A dictionary is created then, with key as genre of book and book deatils appended for each genre, sorted by rating of the book, which is then written to a pickle file -> ***book_data.pkl***. Chatbot gets data from the pickle file.

This chatbot is meant to serve following use cases: 

  - List few genres on request
  - suggest upto three books for asked genre
  - give the name of the author of the book 
  - give the url of the book by appending the isbn no. to https:/openlibrary.org/
  
  Otherwise, it checks the sentiment of the user input to respond accordingly

It also handles other salutations like-> greetings(hello, bye and thank you)

### Dependencies:
  - fuzzywuzzy
  - nltk
  - numpy
  - nltk.sentiment.vader
  - nltk.corpus
  
**Note** Type bye or its synonyms to exit from the chatbot

### Sample
```
Welcome to chatbot
You:hi
Book Asst:hi there! I am book assistant. I can recommend books on genre. What can I do for you?
You:list me some books on religion
Book Asst:For genre Religion I found books:: On Christian Teaching,Erasmus: Ecstasy and the Praise of Folly,Luther and Erasmus: Free Will and Salvation (Library of Christian Classics).
You:link to read the book
Book Asst: Link for your latest search is https:/openlibrary.org/9780664241582.0
You:who is the author
Book Asst: Author for your latest search is Erasmus
You:list me some genres
Book Asst: Few genres that we have are: parenting, anthropology, games, romance, united states
You:list me books on parenting
Book Asst:For genre Parenting I found books:: The Baby Name Wizard: A Magical Method for Finding the Perfect Name for Your Baby,The Wonder of Boys: What Parents, Mentors and Educators Can Do to Shape Boys Into Exceptional Men,The Five Love Languages of Children.
You:who is the author
Book Asst: Author for your latest search is Gary Chapman
You:link ffor the book
Book Asst: Link for your latest search is https:/openlibrary.org/9781881273653.0
You:thank you
Book Asst:See you soon
You:thanks
Book Asst:Mention not
You:bye
Book Asst:bye bye! Happy reading
```
