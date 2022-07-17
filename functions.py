import re
import pandas as pd
import numpy as np
import openpyxl
import os

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    return text


def vectorize_and_find(check_list, input_list):

    complete_list = list(input_list.Name_Cleaned)
    complete_list.extend(list(check_list.Name_Cleaned))

    vect = CountVectorizer(binary=True, ngram_range=(1, 2), analyzer="char")
    vect.fit(list(check_list.Name_Cleaned))
    vectors = vect.transform(complete_list).toarray()

    X = vectors[:input_list.shape[0], :]
    Y = vectors[input_list.shape[0]:, :]

    similarities = cosine_similarity(X, Y)
    all_maxs = np.max(similarities, axis=1)

    found = [list(check_list.iloc[list(
        np.where(similarities[index, :] == percentage)[0]), 0]) if percentage >= 0.0 else ["NOT IN LIST"] for
             index, percentage in enumerate(all_maxs)]

    return list(all_maxs), found

def create_user_dir(path):

    if os.getlogin()!="":
        if (not os.path.exists(rf"{path}\{os.getlogin()}")):

            os.mkdir(rf"{path}\{os.getlogin()}")
            os.mkdir(rf"{path}\{os.getlogin()}\input")
            os.mkdir(rf"{path}\{os.getlogin()}\output")


def get_excel_files_by_user(apppath):

    user_path_absolute = rf"{apppath}\{os.getlogin()}"
    user_path_relative = rf"\static\users\{os.getlogin()}"

    if(os.path.exists(user_path_absolute)):

        input_files = os.listdir(f"{user_path_absolute}\input")
        input_files = [rf"{user_path_relative}\input\{file}" for file in input_files if file.split(".")[-1]=="xlsx"]

        output_files = os.listdir(f"{user_path_absolute}\output")
        output_files = [rf"{user_path_relative}\output\{file}" for file in output_files if file.split(".")[-1] == "xlsx"]

    else:
        input_files = output_files = []


    return  input_files, output_files








