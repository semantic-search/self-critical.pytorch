import json
import uuid
from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache
import init
from caption_service import predict
import globals

def send_to_topic(topic, value_to_send_dic):
    # default=convert only used in this project
    data_json = json.dumps(value_to_send_dic)
    init.producer_obj.send(topic, value=data_json)


if __name__ == "__main__":
    global_init()
    print('main fxn')
    for message in init.consumer_obj:
        message = message.value
        db_key = str(message)
        print(db_key, 'db_key')
        db_object = Cache.objects.get(pk=db_key)
        file_name = db_object.file_name
        init.redis_obj.set(globals.RECEIVE_TOPIC, file_name)
        print('after redis')
        if db_object.is_doc_type:
            """document"""
            print('in doc type')
            images_array = []
            for image in db_object.files:
                pdf_image = str(uuid.uuid4()) + ".jpg"
                with open(pdf_image, 'wb') as file_to_save:
                    file_to_save.write(image.file.read())
                images_array.append(pdf_image)
            captions_list = []
            text_predictions = []
            for image in images_array:
                image_results = predict(image, doc=True)
                captions = image_results["captions"]
                captions_list.append(captions)

            full_res = {
                "container_name": globals.RECEIVE_TOPIC,
                "file_name": file_name,
                "captions": captions_list,
                "is_doc_type": True
            }
            text_res = {
                "container_name": globals.RECEIVE_TOPIC,
                "file_name": file_name,
                "captions": captions_list,
                "is_doc_type": True
            }
            print(full_res, "full_res")
            send_to_topic(globals.SEND_TOPIC_FULL, value_to_send_dic=full_res)
            send_to_topic(globals.SEND_TOPIC_TEXT, value_to_send_dic=text_res)
            init.producer_obj.flush()

        else:
            """image"""
            print('in image type')
            if db_object.mime_type in globals.ALLOWED_IMAGE_TYPES:
                with open(file_name, 'wb') as file_to_save:
                    file_to_save.write(db_object.file.read())
                image_result = predict(file_name)
                response = {
                    "container_name": globals.RECEIVE_TOPIC,
                    "file_name": file_name,
                    "text": image_result["captions"],
                    "is_doc_type": False
                }
                print(response, 'response')
                send_to_topic(globals.SEND_TOPIC_FULL, value_to_send_dic=response)
                send_to_topic(globals.SEND_TOPIC_TEXT, value_to_send_dic=response)
                init.producer_obj.flush()
