import spacy
from tqdm import tqdm, tqdm_notebook

from twitpol import config


def get_nlp():
    stopwords = get_stopwords()
    nlp = spacy.load("en_core_web_lg")
    nlp.Defaults.stop_words.update(stopwords)
    for word in stopwords:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True

    def lemm(doc):
        return lemmatizer(nlp, doc)

    nlp.add_pipe(lemm, name='lemmatizer', after='ner')
    nlp.add_pipe(remove_stopwords, name='stopwords', last=True)

    return nlp


def get_stopwords():
    stopwords = []
    with open(config.DATA / 'sentiment' / 'stopwords.txt') as f:
        lines = f.readlines()
    for i in range(1, len(lines)):
        stopwords.append(lines[i].strip())
    return stopwords


def lemmatizer(nlp, doc):
    """Lemmatize a tweet
    """
    doc = [token.lemma_ for token in doc if token.lemma_ not in ['-PRON-', '\n', '\r', '\n\n', '\r\r']]
    doc = u' '.join(doc)
    return nlp.make_doc(doc)


def remove_stopwords(doc):
    doc = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return doc


def make_docs(docs, nlp, notebook=False):
    if notebook:
        pbar = tqdm_notebook
    else:
        pbar = tqdm
    return [nlp(doc) for doc in pbar(docs)]

