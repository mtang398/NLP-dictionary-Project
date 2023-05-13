import os
from collections import Counter
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from stop_list import closed_class_stop_words
from nltk.stem import PorterStemmer

# Initialize porter stemmer
stemmer = PorterStemmer()

# Download stop words and punkt tokenizer
nltk.download('stopwords')
nltk.download('punkt')

# Load stop words
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])

# Set up directory
cwd = os.getcwd()
CRANFIELD_QRY = os.path.join(cwd, "cran.qry")
CRANFIELD_ALL = os.path.join(cwd, "cran.all.1400")
CRANFIELD_ANS = os.path.join(cwd, "cranqrel")
output = os.path.join(cwd, "output.txt")
testfile = os.path.join(cwd, "test_file.txt")

# Load queries
with open(CRANFIELD_QRY) as f:
    queries = f.read()

queries = queries.split('.I')[1:]
queries = [(q.split('.W\n')[0].strip(), q.split('.W\n')[1].replace('\n', ' ').lower()) for q in queries]

# Load documents
with open(CRANFIELD_ALL) as f:
    documents = f.read()

documents = documents.split('.I')[1:]
documents = [(d.split('.T\n')[0].strip(), d.split('.T\n')[1].replace('\n', ' ').lower()) for d in documents]

# Load stoplist
stop_words.update(closed_class_stop_words)

# Combine queries and documents into a single list of documents
all_docs = queries + documents

# Tokenize each document (while remove all numbers)
tokens_list = []
for d in all_docs:
    tokens = [token for token in word_tokenize(d[1]) if not any(char.isdigit() for char in token)]
    tokens_list.append(tokens)

# Count document frequency for each word
df = Counter()
for tokens in tokens_list:
    df.update(set(tokens + [word for word in stop_words if word in tokens]))

# Compute IDF scores
N = len(all_docs)
idf = {}
for word in df.keys():
    if word in stop_words:
        continue
    idf[word] = math.log(N / df[word])

# Tokenize queries
query_tokens = [word_tokenize(q[1]) for q in queries]

# Count term frequency for each query
tf = []
for tokens in query_tokens:
    tf.append(Counter([t for t in tokens if t not in stop_words]))

# Compute TF-IDF scores for each query (Use log of count)
tfidf = []
for i, query_tf in enumerate(tf):
    query_tfidf = {}
    for word in query_tf.keys():
        if word in idf:
            query_tfidf[word] = (1 + math.log(query_tf[word])) * idf[word]
    tfidf.append(query_tfidf)
    
# Tokenize documents
document_tokens = [word_tokenize(d[1]) for d in documents]

# Count term frequency for each document
document_tf = []
for tokens in document_tokens:
    document_tf.append(Counter([t for t in tokens if t not in stop_words]))

# Compute TF-IDF scores for each document (Use log of count)
document_tfidf = []
for document_tf in document_tf:
    document_tfidf.append({word: (1 + math.log(document_tf[word])) * idf[word] for word in document_tf if word in idf})

def cosine_similarity(tfidf, document_tfidf):
    similarity_scores = []
    for query_tfidf in tfidf:
        scores = []
        for doc_tfidf in document_tfidf:
            # Compute dot product
            dot_product = sum(query_tfidf[word] * doc_tfidf[word] for word in query_tfidf if word in doc_tfidf)
            # Compute magnitudes
            query_magnitude = math.sqrt(sum(query_tfidf[word]**2 for word in query_tfidf))
            doc_magnitude = math.sqrt(sum(doc_tfidf[word]**2 for word in doc_tfidf))
            # Compute cosine similarity
            similarity = dot_product / (query_magnitude * doc_magnitude)
            scores.append(similarity)
        similarity_scores.append(scores)
    return similarity_scores

# Compute cosine similarity between each query and document
similarity_scores = cosine_similarity(tfidf, document_tfidf)

with open(output, 'w') as f:
    for i, query in enumerate(queries):
        scores = similarity_scores[i]
        sorted_docs = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)
        for doc_idx in sorted_docs:
            doc_num = documents[doc_idx][0]
            score = scores[doc_idx]
            f.write(f"{i+1} {doc_num} {score}\n")