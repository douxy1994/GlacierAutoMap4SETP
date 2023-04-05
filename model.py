import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, cohen_kappa_score
from sklearn import model_selection
import pickle
from sklearn.ensemble import  RandomForestClassifier
np.random.seed(6)

def Iris_label(s):
    it={b'0':0, b'1':1}
    return it[s]

path="/data.csv"
SavePath = "/model.pickle"

data=np.loadtxt(path, dtype=float, delimiter=',', converters={7:Iris_label} )

x,y=np.split(data,indices_or_sections=(7,),axis=1)
x=x[:,1:7]

train_data,test_data,train_label,test_label = model_selection.train_test_split(x, y, random_state=1, train_size=0.7,test_size=0.3)
train_data = train_data.astype(np.int16)
test_data = test_data.astype(np.int16)
train_label = train_label.astype(np.int16)
test_label = test_label.astype(np.int16)
print(train_data)
print(train_label)

classification = RandomForestClassifier(n_estimators=250, random_state=1, bootstrap=True, max_depth=120, max_features='sqrt', n_jobs=16)
classification.fit(train_data, train_label.ravel())
pred = classification.predict(test_data)

print("train set：", classification.score(train_data, train_label))
print("test set：", classification.score(test_data, test_label))

f1_score = f1_score(test_label, pred)
cm = confusion_matrix(test_label, pred)
ka = cohen_kappa_score(test_label, pred)

def mean_iou(cf_mtx):
    """
    cf_mtx(ndarray): shape -> (class_num, class_num),
    """
    
    mIou = np.diag(cf_mtx) / (np.sum(cf_mtx, axis=1) + \
                              np.sum(cf_mtx, axis=0) - np.diag(cf_mtx))
    print('===mIou:', mIou)
   
    mIou = np.nanmean(mIou)
    return mIou


miou = mean_iou(cm)
print('miou:', miou)
print('f1_score:', f1_score)
print('cm:', cm)
print('ka:', ka)

file = open(SavePath, "wb")

pickle.dump(classification, file)

file.close()


