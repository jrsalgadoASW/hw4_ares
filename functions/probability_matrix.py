
import string
import numpy as np
from functions.biagram import create_biagram, get_filled_biagram, get_stage_descriptions
from functions.data_cleaning import get_all_characters, get_clean_text
from string_operations import get_character_index, get_number_of_characters
from string_operations import get_number_of_characters

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
def normalize_probabilities(character_count: int, total_characters: int)->float:
    return character_count/total_characters


def get_marginal_probabilities(character_count: dict, text:str)->np.ndarray:
    """
    @input 
        character_count: Dictionary with occurences of each character
        text: the text to analyse
    """
    character_probabilities = np.zeros(len(string.ascii_lowercase))
    n_characters = get_number_of_characters(text)
    for char in character_count.keys():
        index = list(character_count.keys()).index(char)
        character_probabilities[index] = normalize_probabilities(character_count[char], n_characters)+0.00001
    return character_probabilities


def get_cond_probabilities(joint_probability: np.ndarray,marginal_probability: np.ndarray)->np.ndarray:
    conditional_probability = (joint_probability.T/marginal_probability).T
    # normalized matrix
    conditional_probability = conditional_probability/conditional_probability.sum() 
    prob_sum = conditional_probability.sum()
    print(f"prob_sum = {prob_sum}")
    return conditional_probability


def get_joint_probabilities(characters_count: np.ndarray)->np.ndarray:
    all_characters = get_all_characters()
    # + len(all_characters) to account for repetitions (aa, bb, cc, dd, etc.)
    n_pairs = characters_count.sum()
    joint_probability_matrix = create_biagram()
    prob_sum = 0
    for i, row in enumerate(characters_count):
        for j,count in enumerate(characters_count):
            joint_probability_matrix[i][j] = normalize_probabilities(characters_count[i][j], n_pairs)
            prob_sum = prob_sum + joint_probability_matrix[i][j]
    print(f"prob_sum = {prob_sum}")
    return joint_probability_matrix

def graph_matrix_heatmap(matrix: np.ndarray, title="Heatmap"):
    all_characters = get_all_characters()
    # fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(matrix, cmap="Blues" ,annot=False, xticklabels=False, yticklabels=False)
    plt.title(title)
    plt.xticks(rotation=0)
    plt.show()


def language_identifier(text:str, matrix_probabilities: np.ndarray, chosen_stages: list)-> str:

    probs = np.zeros(10)
    clean_text = get_clean_text(text)
    for index in range(0, len(clean_text)-1):
      current_character = clean_text[index]
      next_character = clean_text[index+1]
      
      current_character_index = get_character_index(current_character)
      next_character_index = get_character_index(next_character)

      prob_vector: np.ndarray = np.zeros((10))
      for idx in range(0,10):
        prob_vector[idx] = matrix_probabilities[idx][current_character_index][next_character_index]

      probs = probs + np.log(prob_vector+0.0000001)
    highest_prob_index = np.argmax(probs)
    three_highest = np.argpartition(probs, -3)[-3:]
    res  = chosen_stages[highest_prob_index]
    top3 = []
    top3.append(chosen_stages[three_highest[0]])
    top3.append(chosen_stages[three_highest[1]])
    top3.append(chosen_stages[three_highest[2]])
    return [res,top3]



def get_all_probability_matrices(train_data, chosen_stages: list):
    all_characters = get_all_characters()
    probality_cube:np.ndarray = np.zeros((10,len(all_characters),len(all_characters)))
    for index, stage in enumerate(chosen_stages):
        stage_descriptions = get_stage_descriptions(train_data,stage)
        STAGE_dist = get_filled_biagram(stage_descriptions)
        STAGE_dist = get_joint_probabilities(STAGE_dist)
        probality_cube[index] = STAGE_dist
    return probality_cube