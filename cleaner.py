# cleaner.py
import re
import nltk
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import pandas as pd

# Try to download required NLTK data silently (no exception if offline)
try:
    nltk.data.find("corpora/wordnet")
except Exception:
    try:
        nltk.download("wordnet")
        nltk.download("omw-1.4")
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
    except Exception:
        pass

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(tag):
    """Map NLTK POS tag to wordnet POS constant."""
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    return wordnet.NOUN

def simple_lemmatize(token: str):
    """A small rule-based fallback lemmatizer if wordnet is not available."""
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 4 and token.endswith("ing"):
        return token[:-3]
    if len(token) > 3 and token.endswith("ed"):
        return token[:-2]
    if len(token) > 3 and token.endswith("s"):
        return token[:-1]
    return token

def clean_and_tokenize(text: str):
    """
    Cleans a single text string and returns (clean_text, tokens_list).
    Steps:
      - Lowercase
      - Remove URLs, mentions, hashtags, non-letters
      - Collapse whitespace
      - Remove English stopwords (sklearn's list)
      - Lemmatize using NLTK (POS-aware) with fallback
    """
    if pd.isna(text) or not str(text).strip():
        return "", []

    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[@#]\w+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = text.split()
    tokens = [t for t in tokens if t not in ENGLISH_STOP_WORDS]

    try:
        pos_tags = nltk.pos_tag(tokens)
        lemmas = [lemmatizer.lemmatize(w, get_wordnet_pos(p)) for w, p in pos_tags]
    except Exception:
        lemmas = [simple_lemmatize(t) for t in tokens]

    return " ".join(lemmas), lemmas


def token_analysis(tokens, top_n=20):
    """
    Perform token-level analysis.
    Returns:
      - total_tokens
      - unique_tokens
      - top_tokens (list of tuples)
      - frequency_df (DataFrame)
    """
    if not tokens:
        return 0, 0, [], pd.DataFrame(columns=["token", "frequency"])

    counter = Counter(tokens)

    total_tokens = sum(counter.values())
    unique_tokens = len(counter)
    top_tokens = counter.most_common(top_n)

    freq_df = pd.DataFrame(
        top_tokens, columns=["token", "frequency"]
    )

    return total_tokens, unique_tokens, top_tokens, freq_df

