#!usr/bin/env python3

import json


class Model:
    def __init__(self):
        self._data = self._read_json('exercise_db.json')
        self._exercises_by_category = self._sort_exercises_by_category(self._data)
        self._sorted_categories = sorted(list(self._exercises_by_category.keys()))
        self._sorted_exercise_names = sorted(list(self._data['exercises'].keys()))

    def get_exercise_categories(self):
        return self._sorted_categories

    def get_exercise_names(self):
        return self._sorted_exercise_names

    def get_filtered_exercise_names(self, category):
        return self._exercises_by_category[category]

    def get_exercise_video_links(self, exercise_name):
        return self._data['exercises'][exercise_name]['video links']

    def _read_json(self, file_name):
        with open(file_name, 'r') as infile:
            return json.load(infile)

    def _sort_exercises_by_category(self, data):
        data = self._sort_exercises_into_categories(data)
        data = self._sort_dict_of_lists(data)
        return data

    # returns dict where key is category and value is list of exercises
    def _sort_exercises_into_categories(self, data):
        exercise_by_cat = {}
        for exercise in data['exercises']:
            for category in data['exercises'][exercise]['movement classifications']:
                if category not in exercise_by_cat:
                    exercise_by_cat[category] = [exercise]
                else:
                    exercise_by_cat[category].append(exercise)
        return exercise_by_cat

    def _sort_dict_of_lists(self, data):
        for key in data:
            data[key] = sorted(data[key])
        return data
