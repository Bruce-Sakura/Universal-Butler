from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Embedding, Flatten, Dense

# 假设训练数据集
texts = ["I love this product", "This is terrible", "Amazing experience", "I hate it"]
labels = [1, 0, 1, 0]  # 1表示积极，0表示消极

# 数据预处理
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
X = pad_sequences(sequences, maxlen=100)

# 创建模型
model = Sequential()
model.add(Embedding(input_dim=10000, output_dim=300))  # 输入层
model.add(Conv1D(128, 5, activation='relu'))  # 卷积层
model.add(MaxPooling1D(pool_size=2))  # 池化层
model.add(Flatten())  # 展平层
model.add(Dense(1, activation='sigmoid'))  # 输出层

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 训练模型
model.fit(X, labels, epochs=10, batch_size=32)

# 评估模型
accuracy = model.evaluate(X, labels)
print(f"Model accuracy: {accuracy[1] * 100:.2f}%")

# 测试预测
new_texts = ["I love this movie!", "It was a disaster."]
new_sequences = tokenizer.texts_to_sequences(new_texts)
new_X = pad_sequences(new_sequences, maxlen=100)
predictions = model.predict(new_X)
print(predictions)
