# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.tree import DecisionTreeClassifier


df = pd.read_csv('dataset.csv')

# Rename the column names in the DataFrame.
df.rename(columns = {"t": "bt",}, inplace = True)

# Perform feature and target split
X = df[["sr","rr","bt","lm","bo","rem","sh","hr"]]
y = df['sl']

model = DecisionTreeClassifier(
        ccp_alpha=0.0, class_weight=None, criterion='entropy',
        max_depth=4, max_features=None, max_leaf_nodes=None,
        min_impurity_decrease=0.0, min_samples_leaf=1, 
        min_samples_split=2, min_weight_fraction_leaf=0.0,
        random_state=42, splitter='best'
    )
# Fit the data on model
model.fit(X, y)

# Saving model to disk
pickle.dump(model, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[1, 2, 3, 4, 5, 6, 7, 8]]))