import numpy as np
import pandas as pd
import unittest
from biagram import create_biagram, get_stage_descriptions, get_character_count, get_filled_biagram


def get_all_characters():
    return ['a', 'b', 'c']

def get_character_index(character):
    all_characters = get_all_characters()
    return all_characters.index(character)

class TestBiagram(unittest.TestCase):
    def test_create_biagram(self):
        biagram = create_biagram()
        expected_shape = (3, 3)
        self.assertEqual(biagram.shape, expected_shape)
        self.assertTrue(np.all(biagram == 0))

    def test_get_stage_descriptions(self):
        df = pd.DataFrame({
            'CODIGO_ETAPA': ['A', 'B', 'A', 'C'],
            'DESCRIPCION': ['abc', 'def', 'ghi', 'jkl']
        })
        stage = 'A'
        result = get_stage_descriptions(df, stage)
        expected_result = pd.Series(['abc', 'ghi'])
        pd.testing.assert_series_equal(result, expected_result)

    def test_get_character_count(self):
        descriptions = pd.Series(['abc', 'def', 'ghi'])
        result = get_character_count(descriptions)
        expected_result = {'a': 1, 'b': 1, 'c': 1}
        self.assertDictEqual(result, expected_result)

    def test_get_filled_biagram(self):
        descriptions = pd.Series(['abc', 'def', 'ghi'])
        biagram = get_filled_biagram(descriptions)
        expected_biagram = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        np.testing.assert_array_equal(biagram, expected_biagram)

if __name__ == '__main__':
    unittest.main()
