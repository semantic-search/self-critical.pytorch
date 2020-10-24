# from critical import FeatureExtractor
# import torch
# import captioning
# import captioning.utils.misc
# import captioning.models
# print("in caption searvice code")
# infos = captioning.utils.misc.pickle_load(open('/models/infos_trans12-best.pkl', 'rb'))
# print("in caption searvice code 1")
# feature_extractor = FeatureExtractor()

# print("in caption searvice code 2")
# infos['opt'].vocab = infos['vocab']

# model = captioning.models.setup(infos['opt'])
# model.cuda()
# model.load_state_dict(torch.load('/models/model-best.pth'))

# def get_captions(img_feature):
    # Return the 5 captions from beam serach with beam size 5
    # return model.decode_sequence(model(img_feature.mean(0)[None], img_feature[None], mode='sample', opt={'beam_size':5, 'sample_method':'beam_search', 'sample_n':5})[0])

import requests
import os

def caption_api(file_name):
    with open(file_name, 'rb') as f:
        read_data = f.read()
    files = {
        'file': read_data,
    }
    response = requests.post('http://api/caption/', files=files)
    data = response.content.decode()
    print(data)
    return data

def predict(file_name):

    captions = caption_api(file_name)
    captions = ' '.join(captions)

    os.remove(file_name)

    return captions