import pandas as pd
import numpy as np

from functions import clean_text, vectorize_and_find
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os


def find_names(inputfilepath, outputfilepath):
    # read list of insureds -list of names to check upon-
    check_list = pd.read_excel(inputfilepath, sheet_name="Insureds")

    # read list of names to be checked
    input_template = pd.read_excel(inputfilepath, sheet_name="Claims")

    # cleaning the names on both datasets
    check_list["Name_Cleaned"] = check_list.Name.apply(clean_text)

    input_template["Name_Cleaned"] = input_template.Name.apply(clean_text)

    percentage, name_found = vectorize_and_find(check_list=check_list, input_list=input_template)

    output = pd.DataFrame({
        "Name": input_template.Name,
        "Percentage": percentage,
        "Found_Name": name_found

    })

    output.to_excel(outputfilepath, index=None)


