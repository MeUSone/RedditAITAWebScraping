import operator

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, db
import json, os

load_dotenv()

creds = credentials.Certificate(json.loads(os.environ.get("firebase_auth")))
firebase_admin.initialize_app(creds, {
    'databaseURL': 'https://social-acceptance-fc45b-default-rtdb.firebaseio.com/'})

x = 1

average_c_f = 0
average_c_j = 0
average_j_f = 0

for i in range(1, x + 1):
    ref = db.reference(f'/{i}').get()
    key = list(ref.keys())[0]
    scores_custom_dict = ref[key]["scores_custom"]
    scores_judgement_bot_dict = ref[key]["scores_judgement_bot"]
    max_scores_custom = max(scores_custom_dict.items(), key=operator.itemgetter(1))[0]
    max_scores_judgement_bot = max(scores_judgement_bot_dict.items(), key=operator.itemgetter(1))[0]
    flairs_map = {"Not the A-hole": "NTA", "Asshole": "YTA", "Not Enough Info": "INFO", "Everyone Sucks": "ESH",
                  "No A-holes here": "NAH"}
    flair = ref[key]["flair"]
    mapped_flair = flairs_map[flair]

    if max_scores_custom == mapped_flair:
        average_c_f += 1
    if max_scores_custom == max_scores_judgement_bot:
        average_c_j += 1
    if max_scores_judgement_bot == mapped_flair:
        average_j_f += 1

print("custom algorithm + flair: " + str(round((average_c_f / x) * 100)))
print("custom algorithm + judgement form score: " + str(round(average_c_j / x) * 100))
print("judgement form score + flair: " + str(round(average_j_f / x) * 100))
