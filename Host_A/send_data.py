import kagglehub
from kafka import KafkaProducer
import glob
import json
import base64
import time

path = kagglehub.dataset_download("atifaliak/flower-classification")

# Define paths
image_paths = glob.glob(
    path+'/*/*/*/*.jpg'
)

train_image = list(filter(
    lambda x: x.split('/')[-3]=='train',image_paths
))

mapping_label = {label:i for i,label in enumerate(set(map(lambda x:x.split('/')[-2],train_image)))}


# Define Producer
p=KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer = lambda x: json.dumps(x).encode('utf-8')
)


# Send data
for i in range(len(train_image)):
    p.send(
        'train-data',{
            'data':base64.b64encode(open(train_image[i],'rb').read()).decode('utf-8'),
            'label':mapping_label[train_image[i].split('/')[-2]]
        }
    )
    p.flush()
    time.sleep(1)


