import random

class Word:
    def __init__(self, word, type):
        self.word = word
        self.type = type

all_words = []

happy_file = open("happy.txt", 'r')
sad_file = open("sad.txt", 'r')

for line in happy_file:
    all_words.append(Word(line[:-1].lower(), 'h'))

for line in sad_file:
    all_words.append(Word(line[:-1].lower(), 's'))

happy_file.close()
sad_file.close()

random.shuffle(all_words)

class Organism:
    def __init__(self, seed=None):
        self.chars = {}
        self.score = 0
        for i in range(97, 123): # Every character
            if seed == None:
                self.chars.update({chr(i): random.uniform(-1, 1)})
            else:
                self.chars.update({chr(i): seed.chars[chr(i)] + random.uniform(-0.1, 0.1)})
    def train(self):
        for w in all_words:
            happy_score = 0
            for c in w.word:
                try:
                    happy_score += self.chars[c]
                except:
                    print(c + " is unknown")
            if (happy_score > 0 and w.type == "h") or (happy_score <= 0 and w.type == "s"):
                self.score += 1
    def get_type(self, word):
        hscore = 0
        for c in word:
            hscore += self.chars[c]
        return hscore

organisms = []

for i in range(10):
    organisms.append(Organism())

for i in range(10):
    for o in organisms:
        o.train()

    mx = organisms[0].score
    i = 0
    for o in range(len(organisms)):
        if organisms[o].score > mx:
            mx = organisms[o].score
            i = o

    victor = organisms[i]
    print(victor.score)
    victor.score = 0
    organisms = [victor]

    for i in range(9):
        organisms.append(Organism(seed=victor))

for o in organisms:
    o.train()

mx = organisms[0].score
i = 0
for o in range(len(organisms)):
    if organisms[o].score > mx:
        mx = organisms[o].score
        i = o

print(str(mx) + " / " + str(len(all_words)))

word = input("Enter a word: ")
print(organisms[i].get_type(word))
