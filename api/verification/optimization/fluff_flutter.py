from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def remove_fluff(text: str, extra_fluff=None):
    words = text.split()
    cleaned_words = []

    for i, word in enumerate(words):
        w = word.lower()

        # Remove stopwords
        if w in STOPWORDS:
            continue

        # Remove very short words
        if len(w) <= 2:
            continue

        # Remove repeated words
        if i > 0 and w == words[i - 1].lower():
            continue

        # Remove user-defined fluff
        if extra_fluff and w in extra_fluff:
            continue

        cleaned_words.append(word)

    return " ".join(cleaned_words)