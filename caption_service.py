from critical import FeatureExtractor

import torch
import captioning
import captioning.utils.misc
import captioning.models

import os

infos = captioning.utils.misc.pickle_load(open('/models/infos_trans12-best.pkl', 'rb'))

feature_extractor = FeatureExtractor()

infos['opt'].vocab = infos['vocab']

model = captioning.models.setup(infos['opt'])
model.cuda()
model.load_state_dict(torch.load('/models/model-best.pth'))

def get_captions(img_feature):
    # Return the 5 captions from beam serach with beam size 5
    return model.decode_sequence(model(img_feature.mean(0)[None], img_feature[None], mode='sample', opt={'beam_size':5, 'sample_method':'beam_search', 'sample_n':5})[0])

def predict(file_name, doc=False):

    captions = get_captions(feature_extractor(file_name))
    captions = ' '.join(captions)

    if doc:
        response = {
            "captions": captions
         }
    else:
        response = {
            "file_name": file_name,
            "captions": captions,
            "is_doc_type": False
        }

    os.remove(file_name)

    return response