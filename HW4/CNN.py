import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

class NeuralNetwork(object):

    def __init__(self, n_classes, n_features, n_hidden_units=30,
                 l1=0.0, l2=0.0, epochs=500, learning_rate=0.01,
                 n_batches=1, random_seed=None):

        if random_seed:
            np.random.seed(random_seed)
        self.n_classes = n_classes
        self.n_features = n_features
        self.n_hidden_units = n_hidden_units
        self.w1, self.w2 = self._init_weights()
        self.l1 = l1
        self.l2 = l2
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.n_batches = n_batches

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
#            print(X)
            X_new[1:, :] = X
#            print(X_new)
        return X_new
    
    def _sigmoid(self, X, deriv=False):
        one = np.ones(X.shape, dtype=np.float)
#        print(np.subtract(one, X))
        if deriv:
            return np.multiply(X, np.subtract(one, X))
        return np.divide(one, (np.add(one, np.exp(np.negative(X)))))

    def _forward(self, X):
        net_input = self._add_bias_unit(X, how='column')
#        print(self.w1)
        net_hidden = self.w1.dot(net_input.T)
#        print(self.w1)
        act_hidden = self._sigmoid(net_hidden)
        act_hidden = self._add_bias_unit(act_hidden, how='row')
        net_out = self.w2.dot(act_hidden)
#        print(act_hidden)
        act_out = self._sigmoid(net_out)
        return net_input, net_hidden, act_hidden, net_out, act_out
    
    def _backward(self, net_input, net_hidden, act_hidden, act_out, y):
        sigma3 = np.subtract(act_out, y)
        net_hidden = self._add_bias_unit(net_hidden, how='row')
        sigma2 = self.w2.T.dot(sigma3) * self._sigmoid(net_hidden, True)
        sigma2 = sigma2[1:, :]
        grad1 = sigma2.dot(net_input)
        grad2 = sigma3.dot(act_hidden.T)
        return grad1, grad2

    def _error(self, y, output):
        l1_term = self._l1_reg_loss(self.l1, self.w1, self.w2)
        l2_term = self._l2_reg_loss(self.l2, self.w1, self.w2)
        error = self._cross_entropy(output, y) + l1_term + l2_term
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
        net_input, net_hidden, act_hidden, net_out, act_out = self._forward(X)
        y = y.T

        grad1, grad2 = self._backward(net_input, net_hidden, act_hidden, act_out, y)
#        print(grad1)
        grad1 = pd.DataFrame(grad1)
        grad2 = pd.DataFrame(grad2)
        
        # regularize
        w1 = pd.DataFrame(self.w1)
        w2 = pd.DataFrame(self.w2)
        
        grad1.iloc[:, 1:] += (w1.iloc[:, 1:] * (self.l1 + self.l2))
        grad2.iloc[:, 1:] += (w2.iloc[:, 1:] * (self.l1 + self.l2))
        if count <= 2:
            print(grad1.as_matrix())
        error = self._error(y, act_out)
        
        return error, grad1.as_matrix(), grad2.as_matrix()
    
    def _one_hot(self, y, n_classes):
        one_hot_encoded = pd.get_dummies(y)
        return one_hot_encoded

    def _cross_entropy(self, t, y):
        return -np.sum(np.multiply(t, np.log(y)) + np.multiply((1-t), np.log(1-y)))
    
    def _softmax(self, out):
        log = np.exp(out)
        return log / np.sum(log, axis=1, keepdims=True)
    
    def predict(self, X):
        Xt = X.copy()
        net_input, net_hidden, act_hidden, net_out, act_out = self._forward(Xt)
        return mle(net_out.T)
    
    def predict_proba(self, X):
        Xt = X.copy()
        net_input, net_hidden, act_hidden, net_out, act_out = self._forward(Xt)
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
                epoch_errors.append(error)
#                if count <= 2:
#                    print(self.w1)
#                    print(self.learning_rate)
#                    print(grad1)
                self.w1 = np.subtract(self.w1, self.learning_rate * grad1)
                self.w2 = np.subtract(self.w2, self.learning_rate * grad2)
            self.error_.append(np.mean(epoch_errors))
        return self
    
    def score(self, X, y):
        y_hat = self.predict_proba(X)
        return y_hat
#        return np.sum(y == y_hat, axis=0) / float(X.shape[0])



names = pd.read_csv('input/ingredients.txt', sep='\n')
names = list(names.columns)
names = names[:-1]
names.append('label')
f = open('input/training.csv')
lines = f.readlines()
X = pd.DataFrame(0, index=np.arange(len(lines)), columns=names)
for i, line in enumerate(lines):
    d = line.strip('\n').split(',')
    X.loc[i, 'label'] = d[1].strip('"')
    for ing in d[2:]:
        ing = ing.strip('"')
        if ing in names:
            X.loc[i, ing] = 1
y = X['label']
if 'label' in X.columns:
    X = X.drop('label', axis=1)

net = NeuralNetwork(n_classes=len(y.unique()),
                   n_features=len(X.columns),
                   n_hidden_units=50,
                  l2=0.5,
                  l1=0.0,
                  epochs=300,
                  learning_rate=0.001,
                  n_batches=25,
                  random_seed=123)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
net.fit(X_train, y_train)
s = net.score(X_test, y_test)
print(s)