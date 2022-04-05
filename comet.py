import pandas as pd
import numpy as np
import nltk
from nltk.tag.stanford import StanfordNERTagger
import ast
from collections import defaultdict
import spacy
nlp = spacy.load('en_core_web_lg')
import os
import statistics
from comet2.comet_model import PretrainedCometModel
import pickle
import random
import spacy

comet_model = PretrainedCometModel(device=0)

jar = 'stanford-ner-2020-11-17/stanford-ner.jar'
model = 'stanford-ner-2020-11-17/classifiers/english.conll.4class.distsim.crf.ser.gz'
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

def getCharacters(text):
    unwanted = ['Instagram', 'Christmas', 'AITA','‘']
    words = nltk.word_tokenize(text)
    characters = [i for i in ner_tagger.tag(words) if (i[1] == 'PERSON') and (i[0] not in unwanted)]
    return set(characters)

def getPron(para,document,clusters):
    rt = []
    characters = [i[0] for i in getCharacters(para)]
    female_pron = ["She", "she", "Her", "her"]
    male_pron = ["He", "he", "him", "Him"]
    unresolved_pron = ["I", "Me", "me"]
    other_pron = ["They","they","them", "Them"]
    characters = characters + female_pron + male_pron + unresolved_pron + other_pron
    for i in clusters:
        for j in i:
            ent = " ".join(document[j[0]:j[1] + 1])
            if (ent in characters):
                rt.append(i)
                break

    return rt

def seePron(document, pron):

    n = 0
    doc = {}
    for obj in document:
        doc.update({n: obj})
        n = n + 1

    clus_all = []
    cluster = []
    for i in range(0, len(pron)):
        one_cl = pron[i]
        for count in range(0, len(one_cl)):
            obj = one_cl[count]
            for num in range((obj[0]), (obj[1] + 1)):
                for n in doc:
                    if num == n:
                        cluster.append(doc[n])
        clus_all.append(cluster)
        cluster = []
    return clus_all


def getObjSts(sentence, document, clusters):
    doc = nlp(sentence)
    token_dependencies = [(token.text, token.dep_, token.head.text) for token in doc]
    clus = getPron(sentence, document, clusters)

    start = 0
    end = 0
    rec = []

    while (end < len(token_dependencies)):
        if (token_dependencies[end][0] != "."):
            end += 1
            continue
        else:
            count = 0
            entities = []
            for i in clus:

                for j in i:

                    if (j[0] > end):
                        break
                    if (start <= j[0] and j[0] <= end):
                        entities.append((j[0], j[1] - j[0] + 1))

            uni_ent = {}
            for tup in entities:
                if tup[0] not in uni_ent:
                    uni_ent[tup[0]] = tup[1]
                elif (uni_ent[tup[0]] < tup[1]):
                    uni_ent[tup[0]] = tup[1]
            sorted(uni_ent.items(), key=lambda item: item[0])
            for i in uni_ent:
                if (start <= i and i <= end):
                    count += 1
            rec.append(count)
            start = end
            end += 1

    sts = sentence.split(".")

    rt = []
    selected = [num for num, i in enumerate(rec) if i >= 2]
    for i in selected:
        rt.append(sts[i])
    return rt, clus, seePron(document, clus)

def getDict(txt, mode):

    attrDict = []
    xrDict = []
    orDict = []

    wt_dict = []
    nd_dict = []
    it_dict = []
    cnt = 0
    infs = {"sentence": [], "string": [], "lls": []}

    for st in txt:

        cnt += 1


        if mode == "xAttr":
            inference = comet_model.predict(st, "xAttr", num_beams=5)
            infs["sentence"].append(st)
            infs['string'].append(inference[0])
            infs['lls'].append(inference[1].detach().numpy())
    return infs

def getSentenceAll(filename):
    df = pd.read_csv(filename)
    print(len(set(df["text"])))
    df.drop_duplicates(subset=["text"], inplace=True, keep="first")
    df.reset_index(drop=True, inplace=True)
    print(len(df))
    df = df[:5]

    for a in range(len(df)):
        df["cluster"][a] = ast.literal_eval(str(df["cluster"][a]))
        df["document"][a] = ast.literal_eval(str(df["document"][a]))
        df["clusters"][a] = ast.literal_eval(str(df["clusters"][a]))

    df["ObjSts"] = 0
    df["mainChar_number"] = 0
    df["mainChar_string"] = 0
    df["comet"] = 0
    for a in range(len(df)):
        result = getObjSts(df["text"][a], df["document"][a], df["clusters"][a])
        df["ObjSts"][a] = result[0]
        df["mainChar_number"][a] = result[1]
        df["mainChar_string"][a] = result[2]
        df["comet"][a] = [getDict(result[0],"xAttr")]
        print(a)

    df.to_csv(filename[16:-4] + "_charSts.csv")

getSentenceAll("coreference_csv/coreference_05.csv")









