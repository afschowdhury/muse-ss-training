import pandas as pd


def mujib_relevant_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    ques_df = df[['Q1', 'Q2', 'Q3', 'Q4', 'Mujib Relevant']]
    mujib_relevant_ques = ques_df[ques_df['Mujib Relevant'] == "YES"]
    q1 = mujib_relevant_ques['Q1'].dropna()
    q2 = mujib_relevant_ques['Q2'].dropna()
    q3 = mujib_relevant_ques['Q3'].dropna()
    q4 = mujib_relevant_ques['Q4'].dropna()

    return q1, q2, q3, q4


def all_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    ques_df = df[['Q1', 'Q2', 'Q3', 'Q4']]
    q1 = ques_df['Q1'].dropna()
    q2 = ques_df['Q2'].dropna()
    q3 = ques_df['Q3'].dropna()
    q4 = ques_df['Q4'].dropna()

    return q1, q2, q3, q4

def number_of_questions(qs):
    for i,q in enumerate(qs):
        print(f"Total Q{i+1} : {len(q)}")
        

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
