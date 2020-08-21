from critical import FeatureExtractor

import torch
import captioning
import captioning.utils.misc
import captioning.models

# imports for env kafka
from dotenv import load_dotenv
from kafka import  KafkaProducer
from kafka import KafkaConsumer
from json import loads
import base64
import json
import os

load_dotenv()

KAFKA_HOSTNAME = os.getenv("KAFKA_HOSTNAME")
KAFKA_PORT = os.getenv("KAFKA_PORT")

RECEIVE_TOPIC = 'SELF_CRITICAL'
SEND_TOPIC_FULL = "IMAGE_RESULTS"
SEND_TOPIC_TEXT = "TEXT"

print(f"kafka : {KAFKA_HOSTNAME}:{KAFKA_PORT}")

# To receive img data to process
consumer_self_critical = KafkaConsumer(
    RECEIVE_TOPIC,
    bootstrap_servers=[f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)

# For Sending processed img data further 
producer = KafkaProducer(
    bootstrap_servers=[f"{KAFKA_HOSTNAME}:{KAFKA_PORT}"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)


infos = captioning.utils.misc.pickle_load(open('/models/infos_trans12-best.pkl', 'rb'))

feature_extractor = FeatureExtractor()

infos['opt'].vocab = infos['vocab']

model = captioning.models.setup(infos['opt'])
model.cuda()
model.load_state_dict(torch.load('/models/model-best.pth'))

def get_captions(img_feature):
    # Return the 5 captions from beam serach with beam size 5
    return model.decode_sequence(model(img_feature.mean(0)[None], img_feature[None], mode='sample', opt={'beam_size':5, 'sample_method':'beam_search', 'sample_n':5})[0])

for message in consumer_kerasocr:
    print('xxx--- inside consumer_kerasocr---xxx')
    print(f"kafka - - : {KAFKA_HOSTNAME}:{KAFKA_PORT}")

    
    message = message.value
    image_id = message['image_id']
    data = message['data']

    data = base64.b64decode(data.encode("ascii"))

    captions = get_captions(feature_extractor(data))
    captions = ' '.join(captions)
    response = {
        'image_id': image_id,
        'data': captions
    }
    
    # sending full and text res(without cordinates or probability) to kafka
    producer.send(SEND_TOPIC_FULL, value=response)
    producer.send(SEND_TOPIC_TEXT, value=response)

    producer.flush()
