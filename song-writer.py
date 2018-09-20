# Step 1. Collect all ngrams from a song, adding an start-of-line and
# end-of-line tokens at the start/end of each line.

import nltk
from nltk import *

ngram_list = []
with open("coldplay.txt", "r") as f:
	for line in f.readlines():
		if line.strip():
			bigrams_list = bigrams(word_tokenize(line), pad_left=True,
				                   pad_right=True, left_pad_symbol='<s>',
				                   right_pad_symbol='</s>')
			ngram_list += list(bigrams_list)

#print(ngram_list[:20])

# Step 2. Do frequency distribution and save ngrams to a file because
# we don't want to collect them over and over again.

fd = FreqDist(ngram_list)
print(list(fd.items())[:20])

with open("coldplay-ngrams.txt", "w") as f:
	print(fd.most_common())
	for key, value in fd.most_common():
		print(key)
		f.write("{} {} ~ {}\n".format(key[0], key[1], value))

# check the file now

# Step 3. Read ngrams in a useful data structure. Since we are doing
# generation, we can save 10 most frequent words that follow the word
# in question.

from collections import defaultdict

next_words = defaultdict(list)

with open("coldplay-ngrams.txt", "r") as f:
	for line in f.readlines():
		ngram, freq = line.split(" ~ ")
		first_word, next_word = ngram.split()
		if len(next_words[first_word]) < 10:
			next_words[first_word].append(next_word)

print(next_words["rain"])

# Step 4. Generate one line of song, randomly selecting each new word.

import random

def generate_song_line(first_word):
	"""Generate a sentence using the first word."""
	global next_words
	sentence = [first_word]
	while True: #len(sentence) < 10:
		candidates = next_words[first_word]
		if candidates:
			next_word = random.choice(candidates)
			sentence.append(next_word)
			if next_word == "</s>":
				return " ".join(sentence)
		else:
			return None
		first_word = next_word
	return " ".join(sentence)

print(generate_song_line("I"))


# Step 5. Generate four lines of song.

def generate_song(first_word):
	song = []
	while len(song) < 4:
		line = generate_song_line(first_word)
		if line:
			song.append(line)
			first_word = "<s>"
		else:
			return "The line cannot be generated. Try another word."
	return "\n".join(song)

print(generate_song("<s>"))


