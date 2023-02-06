# data_cleaning.py
"""
Module Docstring: Module for data cleaning.
"""
import string
import pandas as pd
import unidecode


def get_all_characters() -> list:
    """
    @returns all the characters relevant for the model. Right now it is all the printable characters
    """
    all_characters: list = []
    all_letters: list = list(string.ascii_letters)
    all_digits = ["0","1","2","3","4","5","6","7","8","9"]
    printable_characters = list(string.printable)
    all_characters = printable_characters
    #all_characters = all_letters+all_digits
    return all_characters

def get_all_stages(df: pd.DataFrame):
    res = df["CODIGO_ETAPA"].unique() 
    return res

def get_relevant_columns_names() -> list:
    column_labels = ["CODIGO_ETAPA", "DESCRIPCION", "DURACION_HORAS"]
    relevant_columns_names = [column_labels["CODIGO_ETAPA"], column_labels["DESCRIPCION"], column_labels["DURACION_HORAS"]]
    return relevant_columns_names

def get_clean_text(text: str) -> str:
    """
    @return string with only relevant characters to the model
    """
    all_characters = get_all_characters()
    text = unidecode.unidecode(text)
    character_list = list(text)

    for char in character_list:
        if char not in all_characters:
            text = text.replace(char, "")
    return text


def get_relevant_columns(df: pd.DataFrame):
    rcn = get_relevant_columns_names()
    return df[rcn]