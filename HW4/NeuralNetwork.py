import pandas as pd
import numpy as np
from sklearn.model_selection import ShuffleSplit


class NeuralNetwork(object):
    
    def __init__(self, classes, n_features, n_hidden_units=30,
                 l1=0.0, l2=0.0, epochs=500, learning_rate=0.01,
                 n_batches=1, random_seed=None):
        if random_seed:
            np.random.seed(random_seed)
        self.classes = classes
        self.n_classes = len(classes)
        self.n_features = n_features
        self.n_hidden_units = n_hidden_units
        self.n_batches = n_batches
        self.w1, self.w2 = self._init_weights()
        self.l1 = l1
        self.l2 = l2
        self.epochs = epochs
        self.learning_rate = learning_rate

    def _init_weights(self):
        w1 = np.random.uniform(-1.0, 1.0,
                               size=self.n_hidden_units * (self.n_features + 1))
        w1 = w1.reshape(self.n_hidden_units, self.n_features + 1)
        w2 = np.random.uniform(-1.0, 1.0,
                               size=self.n_classes * (self.n_hidden_units + 1))
        w2 = w2.reshape(self.n_classes, self.n_hidden_units + 1)
        return w1, w2

    def _add_bias_unit(self, X, how='column'):
        if how == 'column':
            X_new = np.ones((X.shape[0], X.shape[1] + 1))
            X_new[:, 1:] = X
        elif how == 'row':
            X_new = np.ones((X.shape[0] + 1, X.shape[1]))
            X_new[1:, :] = X
        return np.nan_to_num(X_new)

    def _sigmoid(self, X, count, deriv=False):
        X = X.astype(dtype='float128')
        one = np.ones(X.shape, dtype='float128')
        if deriv:
            return np.multiply(X, np.subtract(one, X))
            # if count <= 4:
            # print"THIS IS NEG X", count, type(np.negative(X)), np.negative(X))
        return np.nan_to_num(np.divide(one, (np.add(one, np.exp(np.negative(X))))))

    def _forward(self, X, count):
        net_input = self._add_bias_unit(X, how='column')
        if count == 90000:
            print("THIS IS W1", count, type(self.w1), self.w1)
        net_hidden = self.w1.dot(net_input.T)
        if count == 90000:
            print("THIS IS NET HIDDEN", count, type(net_hidden), net_hidden)
        act_hidden = self._sigmoid(net_hidden, count=count)
        if count == 90000:
            print("THIS IS ACT HIDDEN", count, type(act_hidden), act_hidden)
        act_hidden = self._add_bias_unit(act_hidden, how='row')
        if count == 90000:
            print("THIS IS W2", count, self.w2)
        net_out = self.w2.dot(act_hidden)
        if count == 90000:
            print("THIS IS ACT HIDDEN AFTER BIAS", count, type(act_hidden), act_hidden)
            print("THIS IS NET OUT", count, net_out)
        #        #printact_hidden)
        act_out = self._sigmoid(net_out, count=count)
        # print"THIS IS ACT OUT IN FORWARD", count, act_out)
        return np.nan_to_num(net_input), np.nan_to_num(net_hidden), np.nan_to_num(act_hidden), np.nan_to_num(
            net_out), np.nan_to_num(act_out)

    def _backward(self, net_input, net_hidden, act_hidden, act_out, y, count):
        sigma3 = np.subtract(act_out, y)
        net_hidden = self._add_bias_unit(net_hidden, how='row')
        sigma2 = self.w2.T.dot(sigma3) * self._sigmoid(net_hidden, deriv=True, count=count)
        sigma2 = sigma2[1:, :]
        grad1 = sigma2.dot(net_input)
        grad2 = sigma3.dot(act_hidden.T)
        # print'THIS IS ACT_OUT IN BACKWARD', act_out)
        # print'THIS IS Y IN BACKWARD', y)
        return np.nan_to_num(grad1), np.nan_to_num(grad2)

    def _error(self, y, output):
        l1_term = self._l1_reg_loss(self.l1, self.w1, self.w2)
        l2_term = self._l2_reg_loss(self.l2, self.w1, self.w2)
        error = self._cross_entropy(output, y)
        return 0.5 * np.mean(error)

    def _l1_reg_loss(self, reg_lambda, w1, w2):
        w1_loss = 0.5 * reg_lambda * np.sum(np.abs(w1))
        w2_loss = 0.5 * reg_lambda * np.sum(np.abs(w2))
        return w1_loss + w2_loss

    def _l2_reg_loss(self, reg_lambda, w1, w2):
        w1_loss = 0.5 * reg_lambda * np.sum(w1 ** 2)
        w2_loss = 0.5 * reg_lambda * np.sum(w2 ** 2)
        return w1_loss + w2_loss

    def _backprop_step(self, X, y, count):
        net_input, net_hidden, act_hidden, net_out, act_out = self._forward(X, count)
        y = y.T

        grad1, grad2 = self._backward(net_input, net_hidden, act_hidden, act_out, y, count)
        # print"THIS IS GRAD2 FROM BACKWARD IN BACKPROP", grad2)

        grad1 = pd.DataFrame(grad1)
        grad2 = pd.DataFrame(grad2)

        # regularize
        w1 = pd.DataFrame(self.w1)
        w2 = pd.DataFrame(self.w2)
        # print'THIS IS GRAD2 ILOC : 1: IN BACKPROP', np.add(grad2.iloc[:, 1:], w2.iloc[:, 1:] * self.l1 + self.l2))

        grad1.iloc[:, 1:] = np.add(grad1.iloc[:, 1:], w1.iloc[:, 1:] * (self.l1 + self.l2))
        grad2.iloc[:, 1:] = np.add(grad2.iloc[:, 1:], w2.iloc[:, 1:] * (self.l1 + self.l2))
        # print"THIS IS W2 AFTER ILOC IN BACKPROP", w2.iloc[:, 1:] * (self.l1 + self.l2))
        # print"THIS IS GRAD2 AFTER ILOC IN BACKPROP", grad2)
        error = self._error(y, act_out)
        # print('error', error)
        # print('THE ERROR', error)

        return error, np.nan_to_num(grad1.as_matrix()), np.nan_to_num(grad2.as_matrix())

    def _one_hot(self, y, n_classes):
        one_hot_encoded = pd.get_dummies(y)
        return one_hot_encoded

    def _cross_entropy(self, y, t):
        return -np.sum(np.multiply(t, np.log(y)) + np.multiply((1 - t), np.log(1 - y)))

    def _softmax(self, out):
        log = np.exp(out)
        return log / np.sum(log, axis=1, keepdims=True)

    def predict(self, X):
        Xt = X.copy()
        net_input, net_hidden, act_hidden, net_out, act_out = self._forward(Xt, 9)
        return self.classes[np.argmax(net_out.T, axis=1)]

    def predict_proba(self, X):
        Xt = X.copy()
        net_input, net_hidden, act_hidden, net_out, act_out = self._forward(Xt, 9)
        return self._softmax(act_out.T)
    
    def fit(self, X, y):
        self.error_ = []
        X_data, y_data = X.copy(), y.copy()
        y_data_enc = self._one_hot(y_data, self.n_classes)
        count = 0
        for i in range(self.epochs):
            X_mb = np.array_split(X_data, self.n_batches)
            y_mb = np.array_split(y_data_enc, self.n_batches)
            epoch_errors = []
            for Xi, yi in zip(X_mb, y_mb):
                count += 1
                # update weights
                error, grad1, grad2 = self._backprop_step(Xi, yi, count)
                # print"THIS IS GRAD2 BEFORE SETTING IN FIT", grad2)
                # print"THIS IS W2 IN FIT", self.w2)
                epoch_errors.append(error)
                #                if count <= 4:
                #                    #printself.w1)
                #                    #printself.learning_rate)
                #                    #printgrad1)
                yi_pred = self.classes[np.argmax(self.predict_proba(Xi), axis=1)]
                if not np.array_equal(yi_pred, yi):
                    self.w1 = np.subtract(self.w1, self.learning_rate * grad1)
                    self.w2 = np.subtract(self.w2, self.learning_rate * grad2)
                # print"THIS IS GRAD2 AFTER SETTING IN FIT", grad2)
            self.error_.append(np.mean(epoch_errors))
            # print("THE ERROR", self.error_)
        return self

    def score(self, X, y):
        y_hat = self.predict(X)
        return 1 - np.sum(y == y_hat) / float(X.shape[0])
    
    def mean_error(self):
        return np.mean(self.error_)



names = pd.read_csv('input/ingredients.txt', sep='\n')
names = list(names.columns)
names = names[:-1]
names.append('label')
f = open('input/training.csv')
lines = f.readlines()
df = pd.DataFrame(0, index=np.arange(len(lines)), columns=names)
for i, line in enumerate(lines):
    d = line.strip('\n').split(',')
    df.loc[i, 'label'] = d[1].strip('"')
    for ing in d[2:]:
        ing = ing.strip('"')
        if ing in names:
            df.loc[i, ing] = 1
y = df['label']
X = df.loc[:, df.columns != 'label']
classes = np.unique(y)


net = NeuralNetwork(classes=classes,
                    n_features=len(X.columns),
                    n_hidden_units=200,
                    l2=0.5,
                    l1=0.0,
                    epochs=300,
                    learning_rate=0.01,
                    n_batches=25,
                    random_seed=0)
ss = ShuffleSplit(n_splits=6, test_size=0.25, random_state=0)
for train, test in ss.split(X):
    net.fit(X.iloc[train], y.iloc[train])
    score = net.score(X.iloc[test], y.iloc[test])
    error = 1 - score
    print(score, error)
    
