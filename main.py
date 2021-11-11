import random, time

class Word:
    def __init__(self, word, type):
        self.word = word
        self.type = type

all_words = []

stime = time.time()

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
        self.past_chars = {}
        self.future_chars = {}
        self.score = 0
        self.evolve_rate = 12
        for i in range(97, 123): # Every character
            if seed == None:
                self.chars.update({chr(i): random.uniform(-self.evolve_rate, self.evolve_rate)})
                self.past_chars.update({chr(i): random.uniform(-self.evolve_rate, self.evolve_rate)})
                self.future_chars.update({chr(i): random.uniform(-self.evolve_rate, self.evolve_rate)})
            else:
                self.chars.update({chr(i): seed.chars[chr(i)] + random.uniform(-self.evolve_rate, self.evolve_rate)})
                self.past_chars.update({chr(i): seed.past_chars[chr(i)] + random.uniform(-self.evolve_rate, self.evolve_rate)})
                self.future_chars.update({chr(i): seed.future_chars[chr(i)] + random.uniform(-self.evolve_rate, self.evolve_rate)})
    def train(self):
        for w in all_words:
            happy_score = 0
            l = len(w.word)
            for i in range(l):
                try:
                    happy_score += self.chars[w.word[i]]
                    if i != 0:
                        happy_score += self.past_chars[w.word[i-1]]
                    if i != l-1:
                        happy_score += self.future_chars[w.word[i+1]]
                except:
                    print(w.word[i] + " is unknown")
            if (happy_score > 0 and w.type == "h") or (happy_score <= 0 and w.type == "s"):
                self.score += 1
    def get_type(self, word):
        hscore = 0
        l = len(word)
        for i in range(l):
            hscore += self.chars[word[i]]
            if i != 0:
                hscore += self.past_chars[word[i]]
            if i != l-1:
                hscore += self.future_chars[word[i+1]]
        return hscore

organisms = []

onum = 50

for i in range(onum):
    organisms.append(Organism())

for i in range(1000):
    for o in organisms:
        o.train()

    mx = organisms[0].score
    i = 0
    for o in range(len(organisms)):
        if organisms[o].score > mx:
            mx = organisms[o].score
            i = o

    print("MAX: " + str(mx))

    victor = organisms[i]
    victor.score = 0
    organisms = [victor]

    for i in range(onum-1):
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
print("TIME: " + str(time.time() - stime))

while True:
    word = input("Enter a word: ")
    print(organisms[i].get_type(word))