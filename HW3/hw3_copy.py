import string, math

class DataRow:

	def __init__(self, row):
		self.row = row

	def word_list(self):
		words = self.row[0].translate(None, string.punctuation)
		return words.split()

	def row_feature(self):
		return int(self.row[1][:-1])

	def build_common_words(self, dataset):
		count, common = func_count_word(dataset), []
		for key, value in count.items():
			if value >= 5: common.append(key)
		return sorted(common)

class BayesData:

	def __init__(self, word, idx, features):
		self.word = word
		self.idx = idx
		self.features = features

class Feature:

	def __init__(self, feature, label):
		self.feature = feature
		self.label = label

class Bayessian:

	def __init__(self, word, idx, features):
		self.word = word
		self.idx = idx
		self.features = features

	def count_label(self):
		pos_cnt, neg_cnt = 0, 0
		for feature in self.features:
			if feature.label == 1:
				pos_cnt += 1
			if feature.label == 0:
				neg_cnt += 1
		return pos_cnt, neg_cnt

	def count_feature(self):
		pos_cnt_1, neg_cnt_1 = 0, 0
		pos_cnt_2, neg_cnt_2 = 0, 0
		for feature in self.features:
			if feature.label == 1 and feature.feature[self.idx] == 1: pos_cnt_1 += 1
			if feature.label == 1 and feature.feature[self.idx] == 0: neg_cnt_1 += 1
			if feature.label == 0 and feature.feature[self.idx] == 1: pos_cnt_2 += 1
			if feature.label == 0 and feature.feature[self.idx] == 0: neg_cnt_2 += 1
		return pos_cnt_1, neg_cnt_1, pos_cnt_2, neg_cnt_2

	def fetch_prob(self):
		pos_cnt_1, neg_cnt_1, pos_cnt_2, neg_cnt_2 = self.count_feature()
		pos_cnt, neg_cnt = self.count_label()
		pos_prob_1 = float(pos_cnt_1 + 1) / float(pos_cnt + 2)
		neg_prob_1 = float(neg_cnt_1 + 1) / float(neg_cnt + 2)
		pos_prob_2 = float(pos_cnt_2 + 1) / float(pos_cnt + 2)
		neg_prob_2 = float(neg_cnt_2 + 1) / float(pos_cnt + 2)
		return pos_prob_1, neg_prob_1, pos_prob_2, neg_prob_2

	def calc_prob(self, label):
		pos_cnt, neg_cnt = self.count_label()
		return float(pos_cnt) / (pos_cnt + neg_cnt) if label == 1 else float(neg_cnt) / (pos_cnt + neg_cnt)

def func_load_file(name):
	dataset = []
	with open(name, 'r') as file:
		for item in file:
			line = item.split('\t')
			dataset.append(DataRow(line))
		file.close()
	return dataset

def func_store_file(name, words, features):
	with open(name, 'w') as file:
		for feature in features:
			file.write(feature)
		file.close()

def func_count_word(dataset):
	count = {}
	for datarow in dataset:
		for word in datarow.word_list():
			if word in count: count[word] += 1
			else: count[word] = 1
	return count

def func_build_feature(dataset):
	features = []
	for datarow in dataset:
		tmp_list = []
		for word in datarow.build_common_words(dataset):
			tmp_list.append(1 if word in datarow.word_list() else 0)
		features.append(Feature(tmp_list, datarow.row_feature()))
	return features

def func_train_data(common_words, features):
	bayes_data = {}
	for idx in range(len(common_words)):
		word = common_words[idx]
		bayes_data[word] = Bayessian(word, idx, features)
	return bayes_data

def func_classify_data(common_words, bayes_data, feature):
	pos_cnt, neg_cnt = 0, 0
	for i in range(len(common_words)):
		word = common_words[i]
		pos_prob_1, neg_prob_1, pos_prob_2, neg_prob_2 = bayes_data[word].fetch_prob()
		if feature[i] == 1:
			pos_cnt += math.log(pos_prob_1)
			neg_cnt += math.log(neg_prob_1)
		else:
			pos_cnt += math.log(pos_prob_2)
			neg_cnt += math.log(neg_prob_2)
	word = common_words[0]
	pos_cnt += math.log(bayes_data[word].calc_prob(1))
	neg_cnt += math.log(bayes_data[word].calc_prob(0))
	return 1 if pos_cnt >= neg_cnt else 0

if __name__ == '__main__':
	train_set, test_set = func_load_file('trainingSet.txt'), func_load_file('testSet.txt')
	train_features, test_features, common_features = func_build_feature(train_set), func_build_feature(test_set), func_build_feature(train_set + test_set)
	for i in range(len(common_features)):
		common_words = train_set[i].build_common_words(train_set)
		data = func_train_data(common_words, train_features)
		rs = [func_classify_data(common_words, data, feature.feature) for feature in train_features]
		print rs