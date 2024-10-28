with open('wordlist.txt', 'r') as file:
    contents = file.read()

words = contents.split()
unique_words = set(words)

print(f'Number of unique words: {len(unique_words)}')

with open('wordlist.txt', 'w') as file:
    file.write(' '.join(unique_words))
