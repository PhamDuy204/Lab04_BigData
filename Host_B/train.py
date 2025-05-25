from sklearn.metrics import accuracy_score
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import sys
import numpy as np
import os
import pickle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocessing_img import preprocessing_img
def train_data(batch_df,batch_id,model):
    if batch_df.count() > 100: # train when the number of rows > 100
        eval_train_data=[]
        eval_label = []
        lst = batch_df.collect()
        with ThreadPoolExecutor(max_workers = 8) as executor:
            train_data = np.array(list(executor.map(preprocessing_img, lst)))
            labels = np.array(list(executor.map(lambda x:x['label'], lst)))
            
            model.fit(np.array(train_data),np.array(labels))
            eval_label.extend(labels.tolist())
            eval_train_data.extend(train_data.tolist())
        y_pred=model.predict(np.array(eval_train_data))
        print(f'Batch {batch_id} has training accuracy : {accuracy_score(np.array(eval_label),y_pred)}')
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp',exist_ok=True)
        if not os.path.exists('./checkpoints'):
            os.makedirs('./checkpoints',exist_ok=True)

        with open(f"./tmp/batch_{batch_id}.log", "w") as f:
            f.write(f"Batch {batch_id} has {batch_df.count()} rows\n")
            f.write(f'training_acc : {accuracy_score(np.array(eval_label),y_pred)}')
        with open(f"./checkpoints/model_{batch_id}.pkl", "wb") as f:
            pickle.dump(model, f)
    else:
        print("Don't have enough data for training" )