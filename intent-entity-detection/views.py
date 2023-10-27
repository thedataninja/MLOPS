from flask import Blueprint, request, jsonify
from exceptions import InvalidUsage
import numpy as np
import requests
import logging
from transformers import AutoTokenizer
from collections import defaultdict
import time

model = 'jplu/tf-xlm-roberta-base'
#model = 'distilbert-base-multilingual-cased'
import os
os.environ['CURL_CA_BUNDLE'] = ''
tokenizer = AutoTokenizer.from_pretrained(model)

intent_entity = Blueprint(
    'intent_entity',
    __name__,
    template_folder='templates',
    static_folder='static'
)


def preprocess1(text):

    text = text.strip()
    text = text.replace("?", " ? ")
    text = text.replace("!", " ! ")
    text = text.replace(".", " . ")
    text = text.replace(",", " , ")
    return text

def preprocess(text):

    max_length = 50
    token_ids = np.zeros(shape=(1, max_length),
                         dtype=np.int32)
    # for i, text_sequence in enumerate(text_sequences):
    # print(text_sequence)
    encoded = tokenizer.encode(text,truncation=True,max_length=max_length)
    token_ids[0, 0:len(encoded)] = encoded
    # attention_masks = np.ones(shape=(1,inputs.shape[1]))
    attention_masks = (token_ids != 0).astype(np.int32)
    # return {"input_ids": token_ids, "attention_masks": attention_masks}
    #input_ids_in, input_masks_in
    return {
        "inputs": {"input_ids": token_ids.tolist(),
                   "attention_masks": attention_masks.tolist()
                  }
    }

def decode_predictions(text, intent_id, slot_ids):

    #print(text,intent_id,slot_ids)
    intent_names = ['AddToPlaylist','BookRestaurant','GetWeather','PlayMusic','RateBook','SearchCreativeWork','SearchScreeningEvent']
    #slot_names = ['[PAD]', 'O', 'B-sys.zip-code', 'B-company', 'B-employmentType', 'B-sys.time', 'B-jobType', 'I-jobType', 'I-sys.time', 'B-sys.date', 'I-sys.date', 'B-sys.quantity', 'I-sys.quantity', 'B-sys.phone-number', 'I-sys.phone-number', 'B-sys.ordinal', 'I-sys.ordinal', 'B-sys.number-integer', 'B-degreeName', 'B-sys.location', 'I-degreeName', 'I-sys.location', 'I-company', 'B-sys.language', 'I-employmentType', 'B-sys.currency-name', 'I-sys.currency-name', 'B-person', 'I-person', 'B-ordinal']
    slot_names = ['[PAD]', 'O', 'B-entity_name', 'I-entity_name', 'B-playlist_owner', 'B-playlist', 'I-playlist', 'B-music_item',
     'B-artist', 'I-artist', 'I-playlist_owner', 'B-party_size_number', 'B-sort', 'B-restaurant_type',
     'B-restaurant_name', 'I-restaurant_name', 'B-city', 'B-state', 'I-state', 'B-spatial_relation', 'B-poi', 'I-poi',
     'B-served_dish', 'B-country', 'I-country', 'B-timeRange', 'I-timeRange', 'B-facility', 'B-party_size_description',
     'I-party_size_description', 'I-city', 'I-spatial_relation', 'B-cuisine', 'I-cuisine', 'I-sort',
     'I-restaurant_type', 'I-served_dish', 'I-facility', 'B-geographic_poi', 'I-geographic_poi',
     'B-condition_temperature', 'B-condition_description', 'B-current_location', 'I-current_location', 'B-service',
     'B-year', 'I-service', 'B-album', 'I-album', 'B-genre', 'I-genre', 'B-track', 'I-track', 'I-music_item',
     'B-rating_value', 'B-best_rating', 'B-rating_unit', 'B-object_name', 'I-object_name',
     'B-object_part_of_series_type', 'B-object_select', 'B-object_type', 'I-object_select', 'I-object_type',
     'I-object_part_of_series_type', 'B-movie_name', 'I-movie_name', 'B-object_location_type', 'I-object_location_type',
     'B-location_name', 'I-location_name', 'B-movie_type', 'I-movie_type']

    info = {"intent": intent_names[intent_id]}
    #print("slot-",slot_ids,len(slot_ids))
    #print("word-",text.split() , len(text.split()))
    collected_slots = defaultdict(list)
    active_slot_words = []
    active_slot_name = None
    for word in text.split():
        tokens = tokenizer.tokenize(word)


        current_word_slot_ids = slot_ids[:len(tokens)]

        slot_ids = slot_ids[len(tokens):]

        try:
            current_word_slot_name = slot_names[current_word_slot_ids[0]]
            # print(current_word_slot_name,active_slot_name)
            if current_word_slot_name == "O" or current_word_slot_name == "[PAD]":
                if active_slot_name:
                    collected_slots[active_slot_name].append(" ".join(active_slot_words))
                    active_slot_words = []
                    active_slot_name = None
            else:
                # Naive BIO: handling: treat B- and I- the same...
                new_slot_name = current_word_slot_name[2:]
                if active_slot_name is None:
                    active_slot_words.append(word)
                    active_slot_name = new_slot_name
                elif new_slot_name == active_slot_name:
                    active_slot_words.append(word)
                else:
                    collected_slots[active_slot_name].append(" ".join(active_slot_words))
                    active_slot_words = [word]
                    active_slot_name = new_slot_name
        except:
            break
    if active_slot_name:
        collected_slots[active_slot_name].append(" ".join(active_slot_words))
    info["slots"] = dict(collected_slots)
    return info

@intent_entity.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@intent_entity.route('/', methods=['GET', 'POST'])
#@authentication_required
def get_intent():

    try:
        body = request.get_json(silent=True)
    except:
        raise InvalidUsage('Bad request body missing.', status_code=308)

    start = time.time()
    text_str = body["document"]["content"]
    #basic processing
    #find word len
    word_count = len(text_str.split())
    text_str = preprocess1(text_str)
    json_str = preprocess(text_str)
    #print(json_str)
    resp = requests.post('http://localhost:8501/v1/models/intent_entity:predict', json=json_str)
    print(resp.json())
    output =  resp.json()['outputs']
    print(output)
    intent_logits = output['dense']
    slot_logits = output['dense_1']
    #print(intent_logits[0])

    slot_ids = np.array(slot_logits).argmax(axis=-1)[0, 1:-1]
    #print(slot_ids)
    intent_id = np.array(intent_logits).argmax(axis=-1)[0]
    confidence = intent_logits[0][intent_id]
    info = decode_predictions(text_str,
                                  intent_id, slot_ids)
    #its better to rephrase the question if confidence is low
    end = time.time()
    time_taken = int((end - start) * 1000)
    logging.info(
        "Input text= {}, Intent detected = {}, Entity detected = {}, time taken in milli secs = {}, Confidence = {}".format(text_str,
                                                                                                        info['intent'],
                                                                                                        info['slots'],
                                                                                                        str(
                                                                                                            time_taken),str(confidence)))
    if confidence < .20:
        info['intent'] = ""

    if word_count == 1 and confidence < .85: #if it a one word and confidence is low we return empty
        info['intent'] = ""

    resp.close()
    #logging.info("Input text= {}, Intent detected = {}, Entity detected = {}, time taken = {} milli secs".format(text_str, info['intent'], info['slots'], str(time_taken)))

    my_str =  {
                                        'intent': info['intent'],
                                        'entities': info['slots'],
                                        'confidence': confidence
                }
    return jsonify(my_str)
