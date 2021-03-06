#!/usr/bin/env python3
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy, tflearn, tensorflow, random, pickle, webbrowser, math
nltk.download('punkt')

data = {"intents": [
        {"tag": "greeting",
         "patterns": ["Hi", "How are you", "Is anyone there?", "Hello", "Good day", "Whats up"],
         "responses": ["Hello!", "Good to see you again!", "Hi There"],
         "context_set": ""
        },
        {"tag": "goodbye",
         "patterns": ["cya", "See you later", "Goodbye", "I am Leaving", "Have a Good day"],
         "responses": ["Sad to see you go :(", "Talk to you later", "Goodbye!"],
         "context_set": ""
        },
        {"tag": "age",
         "patterns": ["how old",  "what is your age", "how old are you", "age?"],
         "responses": ["I am less than 1 year old", "1 years young!"],
         "context_set": ""
        },
        {"tag": "name",
         "patterns": ["what is your name", "what should I call you", "whats your name?"],
         "responses": ["I'm your friend", "I'm your friend~ hello there", "I'm Your Friend, Your Chatbot"],
         "context_set": ""
        },
        {"tag": "joke",
          "patterns": ["Tell me a joke", "Tell me something funny", "Make me laugh"],
          "responses": ["What’s the best thing about Switzerland? I don’t know, but the flag is a big plus.", "Why do we tell actors to “break a leg?” Because every play has a cast.", "Helvetica and Times New Roman walk into a bar. “Get out of here!” shouts the bartender. “We don’t serve your type.”", "Yesterday I saw a guy spill all his Scrabble letters on the road. I asked him, “What’s the word on the street?”", 
                        "Hear about the new restaurant called Karma? There’s no menu: You get what you deserve."],
          "context_set": ""
        }, 

        {"tag": "thank you", 
          "patterns": ["thank you", "good joke"], 
          "responses": ["your welcome"],
          "context_set": ""
        }, 
        {"tag": "open", 
          "patterns": ["open website", "open", "website", "web"],
          "responses": ["opening"],
          "context_set": ""
         },
        {"tag": "math",
          "patterns": ["math", "do some math for me", "do some math"],
          "responses":["here is the answer"],
          "context_set": ""
        },
   ]
}

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
  for pattern in intent["patterns"]:
    wrds = nltk.word_tokenize(pattern)
    words.extend(wrds)
    docs_x.append(wrds)
    docs_y.append(intent["tag"])
  if intent["tag"] not in labels:
    labels.append(intent["tag"])


labels = sorted(labels)

words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))

words

training = []
output = []
out_empty = [0 for _ in range(len(labels))]
for x, doc in enumerate(docs_x):
  bag = []
  wrds = [stemmer.stem(w) for w in doc]
  for w in words:
    if w in wrds:
      bag.append(1)
    else:
      bag.append(0)
  output_row = out_empty[:]
  output_row[labels.index(docs_y[x])] = 1
  training.append(bag)
  output.append(output_row)

traning = numpy.array(training)

tensorflow.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

def fib(n):
    d = [1 for x in range(101010)]
    for i in range(2, n+1, 1):
        d[i] = d[i-1] + d[i-2]
    return [1] + sorted(list(set(d)))

def bag_of_words(s, words):
  bag = [0 for _ in range(len(words))]
  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]
  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1

  return numpy.array(bag)

def chat():
  print("Start talking with the bot! type quit to stop")
  while True:
    inp = input("You: ")
    if inp.lower() == "quit" or inp.lower() == "exit":
      break
    
    results = model.predict([bag_of_words(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    for tg in data["intents"]:
      if tg['tag'] == tag:
        responses = tg['responses']
    if tag == "open":
      webget = input("Which webpage to open ")
      webbrowser.open(webget)

    if tag == "math":
      mathget = input("What equation: ")
      try:
        print(eval(mathget))
        
      except:
        print("enter a valid equation")
    print(random.choice(responses))
if __name__ == "__main__":
    chat()


