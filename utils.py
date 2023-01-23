from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import pickle
from sentence_transformers.util import semantic_search
import json
import pandas as pd


# model instantiation

# model_path = "data/model/st-model/16500"
# model_path = "data/model/st-model-1/37500"
# last saved model
model_path = "data/model/st-model-2/12000"
# retriever_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
retriever_model = SentenceTransformer(model_path)


def get_embeddings(sentences):
    embeddings = retriever_model.encode(sentences, convert_to_tensor=True)
    return embeddings


def evaluate(ques, index, base_embeddings, base_index):

    model_idx = []
    for q in ques:
        q_emb = retriever_model.encode(q)
        query_embeddings = torch.FloatTensor(q_emb)
        hits = semantic_search(query_embeddings, base_embeddings, top_k=1)

        # print(hits[0][0]['corpus_id'])
        model_idx.append(hits[0][0]['corpus_id'])

    f_d = []
    for i in range(len(model_idx)):
        f = model_idx[i]
        # if f <= q2_idx[-1]:
        f_d.append(base_index[model_idx[i]])

    count = 0
    for i in range(len(f_d)):
        if f_d[i] == index[i]:
            count += 1

    print(f"Successfully indexed: {count} questions out of {len(index)}")

    model_accuracy = count/len(index)
    print("Models Accuracy : ", model_accuracy)


def mujib_relevant_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    ques_df = df[['Q1', 'Q2', 'Q3', 'Q4', 'Mujib Relevant']]
    mujib_relevant_ques = ques_df[ques_df['Mujib Relevant'] == "YES"]
    q1 = mujib_relevant_ques['Q1'].dropna()
    q2 = mujib_relevant_ques['Q2'].dropna()
    q3 = mujib_relevant_ques['Q3'].dropna()
    q4 = mujib_relevant_ques['Q4'].dropna()

    return q1, q2, q3, q4


def question_context_splitter(qs):
    ques = []

    for q in qs:
        ques.append(q)

    idx = qs.index.tolist()

    return ques, idx


def change_to_mujib(questions):
    mujib_names = ["বঙ্গবন্ধু", "বঙ্গবন্ধুর", "শেখ মুজিবুর রহমান",
                   "শেখ মুজিব",   "জাতির পিতা", "জাতির জনক"]
    changed_question = []
    for question in questions:

        altered_ques = question

        for name in mujib_names:
            altered_ques = altered_ques.replace(name, "মুজিব")

        while "মুজিব মুজিব" in altered_ques:
            altered_ques = altered_ques.replace("মুজিব মুজিব", "মুজিব")
        changed_question.append(altered_ques)

    return changed_question


def bow(sentences):
    from collections import Counter

    word_ls = []

    for sen in sentences:
        word_ls.extend(sen.split())
        # print(len(word_ls))

    print(len(word_ls))

    Counter = Counter(word_ls)
    most_occured_20 = Counter.most_common(20)
    # print(most_occured_20)

    most_occured_50 = Counter.most_common(50)

    return most_occured_20, most_occured_50
