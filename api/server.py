from fastapi import FastAPI, File, UploadFile

from critical import FeatureExtractor

import torch
import captioning
import captioning.utils.misc
import captioning.models
infos = captioning.utils.misc.pickle_load(open('/models/infos_trans12-best.pkl', 'rb'))

feature_extractor = FeatureExtractor()

infos['opt'].vocab = infos['vocab']

model = captioning.models.setup(infos['opt'])
model.cuda()
model.load_state_dict(torch.load('/models/model-best.pth'))

def get_captions(img_feature):
    # Return the 5 captions from beam serach with beam size 5
    return model.decode_sequence(model(img_feature.mean(0)[None], img_feature[None], mode='sample', opt={'beam_size':5, 'sample_method':'beam_search', 'sample_n':5})[0])

app = FastAPI()

@app.post("/caption/")
def create_upload_file(file: UploadFile = File(...)):
    fileName = file.filename

    captions = get_captions(feature_extractor(file.file))

    return ' '.join(captions)
