# 5分类任务
from numpy import asarray
from numpy import zeros
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import time
import matplotlib.pyplot as plt
import pandas as pd
######################################################
start = time.process_time()
##############################################################################
amazon_5_processed = "D:\SoftPackage\pycharm\PyCharmProject\MachineLearning\Data\Amazon-5_processed"
##############################################################################
path_very_neg = amazon_5_processed + "\\very_neg_processed.txt"
path_neg = amazon_5_processed + "\\neg_processed.txt"
path_neutral = amazon_5_processed + "\\neutral_processed.txt"
path_pos = amazon_5_processed + "\pos_processed.txt"
path_very_pos = amazon_5_processed + "\\very_pos_processed.txt"
##############################################################################
# 读取数据
file_very_neg = open(path_very_neg, 'r', encoding='utf-8')
very_neg_comments = file_very_neg.readlines()
file_very_neg.close()

file_neg = open(path_neg, 'r', encoding='utf-8')
neg_comments = file_neg.readlines()
file_neg.close()

file_neutral = open(path_neutral, 'r', encoding='utf-8')
neutral_comments = file_neutral.readlines()
file_neutral.close()

file_pos = open(path_pos, 'r', encoding='utf-8')
pos_comments = file_pos.readlines()
file_pos.close()

file_very_pos = open(path_very_pos, 'r', encoding='utf-8')
very_pos_comments = file_very_pos.readlines()
file_very_pos.close()
##############################################################################
# 读取处理后的数据，把每句末尾的'\n'删除
# very_pos 有2841130，总评论有4542410，去掉892,410个，形成3,650,000条Amazon-5数据
# 去除very_pos中892,410个,因此2,841,130-892,410=1,948,720
processed_very_pos_comments = []
for index,sentence in enumerate(very_pos_comments):
    if index < 1948720:
        data = sentence.split(' ')
        remove_sign = data[len(data) - 1].replace('\n', '')
        data[len(data) - 1] = remove_sign
        processed_very_pos_comments.append(data)

processed_pos_comments = []
for index,sentence in enumerate(pos_comments):
    data = sentence.split(' ')
    remove_sign = data[len(data) - 1].replace('\n', '')
    data[len(data) - 1] = remove_sign
    processed_pos_comments.append(data)

processed_neutral_comments = []
for index,sentence in enumerate(neutral_comments):
    data = sentence.split(' ')
    remove_sign = data[len(data) - 1].replace('\n', '')
    data[len(data) - 1] = remove_sign
    processed_neutral_comments.append(data)

processed_neg_comments = []
for index,sentence in enumerate(neg_comments):
    data = sentence.split(' ')
    remove_sign = data[len(data)-1].replace('\n', '')
    data[len(data)-1] = remove_sign
    processed_neg_comments.append(data)

processed_very_neg_comments = []
for index,sentence in enumerate(very_neg_comments):
    data = sentence.split(' ')
    remove_sign = data[len(data)-1].replace('\n', '')
    data[len(data)-1] = remove_sign
    processed_very_neg_comments.append(data)
# Let's have a look at the processed data information
print(f"len processed very_pos comments: {len(processed_very_pos_comments)}")
print(f"len processed pos comments: {len(processed_pos_comments)}")
print(f"len processed neutral comments: {len(processed_neutral_comments)}")
print(f"len processed neg comments: {len(processed_neg_comments)}")
print(f"len processed very_neg comments: {len(processed_very_neg_comments)}")

a1 = len(processed_very_pos_comments)
b1 = len(processed_pos_comments)
c1 = len(processed_neutral_comments)
d1 = len(processed_neg_comments)
e1 = len(processed_very_neg_comments)
print(f"total: {a1+b1+c1+d1+e1}")
##############################################################################
docs = processed_very_pos_comments+processed_pos_comments +processed_neutral_comments\
       + processed_neg_comments+processed_very_neg_comments
# 5,4,3,2,1
labels = [4 for i in range(len(processed_very_pos_comments))]
labels.extend([3 for i in range(len(processed_pos_comments))])
labels.extend([2 for i in range(len(processed_neutral_comments))])
labels.extend([1 for i in range(len(processed_neg_comments))])
labels.extend([0 for i in range(len(processed_very_neg_comments))])

labels = to_categorical(labels)  # one-hot编码(要求3类及3类以上)，关键
##############################################################################
# 看一下数据分布
fig, ax = plt.subplots()
review_len = [len(x) for x in docs]
pd.Series(review_len).hist()
plt.xlabel('Avg sentence length')
plt.ylabel('Number of sentencens')
plt.show()
# fig.savefig('Amazon-5.png',dpi=900,format='png')
infor = pd.Series(review_len).describe()  # 图表相关信息
print(infor)
##########################################################################
# prepare tokenizer
t = Tokenizer()
t.fit_on_texts(docs)
vocab_size = len(t.word_index) + 1
print(f"vocab_size: {vocab_size}")
##############################################################################
# integer encode the documents
encoded_docs = t.texts_to_sequences(docs)
print(f"encoded_docs: {encoded_docs[:4]}")
##############################################################################
# pad documents to a max length of n words
# max_length = max([len(s.split()) for s in docs])
max_length = max([len(docs[i]) for i in range(len(docs))])
print(f"max_length: {max_length}")

# 根据数据分布，可以发现99%以上的数据是少于500长度
max_length = 500

padded_docs = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
print(f"padded_doc:\n {padded_docs[:4]}")
##############################################################################
# 划分train and test set
# note: random_state让每次划分的训练集和数据集相同
X_train, X_test, y_train, y_test = train_test_split(padded_docs, labels, test_size=0.2,random_state=4)
##############################################################################
path_glove = "D:\SoftPackage\pycharm\PyCharmProject\MachineLearning\Data\\glove.6B.50d.txt"
glove_dim = 50
# load the whole embedding into memory
embeddings_index = dict()
f = open(path_glove, mode='rt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Loaded %s GloVe word vectors.' % len(embeddings_index))
##############################################################################
# create a weight matrix for words in training docs
embedding_matrix = zeros((vocab_size, glove_dim))
for word, i in t.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
##############################################################################
# define model
model = Sequential()
e = Embedding(vocab_size, glove_dim, weights=[embedding_matrix], input_length=max_length, trainable=True)

model.add(e)
model.add(Conv1D(filters=32, kernel_size=8, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
# 全连接层
model.add(Dense(10, activation="relu"))
# 输出层
model.add(Dense(5, activation='softmax'))
##############################################################################
# compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
# fit the model
model.fit(X_train, y_train, epochs=10, verbose=1, batch_size=1000)
##############################################################################
# evaluate the model
loss, acc = model.evaluate(X_train, y_train, verbose=0)
print('train accuracy: %f' % (acc*100))

_, accuracy = model.evaluate(X_test, y_test, verbose=0)
print('test accuracy: %f' % (accuracy*100))
##############################################################################
end = time.process_time()
print(f"running time: {end-start}")
##############################################################################
