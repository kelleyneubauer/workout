#!usr/bin/env python3

import tkinter as tk
import csv
import webbrowser
import workout_builder_model as wbm
import workout_builder_view as wbv


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.model = wbm.Model()
        self.view = wbv.View(self.root)
        self._bind_launch_screen_events()

    def _bind_launch_screen_events(self):
        self._bind_button(self.view.get_save_widget(), self._save_workout)
        self._bind_button(self.view.get_load_widget(), self._load_workout)
        self._bind_button(self.view.get_add_block_widget(), self._add_block)
        self._bind_button(self.view.get_remove_block_widget(), self._remove_block)

    def _bind_button(self, button, handler):
        button.bind('<Button>', handler)

    def _bind_combobox(self, combobox, handler):
        combobox.bind('<<ComboboxSelected>>', handler)

    def _add_block(self, event=None):
        self.view.add_block()
        new_block = self.view.get_last_block()
        self._bind_block_events(new_block)
        return self.view.get_last_block()

    def _bind_block_events(self, block):
        self._bind_button(block.get_add_exercise_widget(),
                          lambda event, group=block:
                          self._add_exercise(event, group))
        self._bind_button(block.get_remove_exercise_widget(),
                          lambda event, group=block:
                          self._remove_exercise(event, group))

    def _add_exercise(self, event, block):
        block.add_exercise()
        new_exercise = block.get_last_exercise()
        self._bind_exercise_events(new_exercise)
        self._initialize_exercise_comboboxes(new_exercise)
        return block.get_last_exercise()

    def _bind_exercise_events(self, exercise):
        self._bind_button(exercise.get_clear_widget(),
                          lambda event, group=exercise:
                          self._clear_onclick(event, group))
        self._bind_button(exercise.get_view_link_widget(),
                          lambda event, group=exercise:
                          self._view_onclick(event, group))
        self._bind_combobox(exercise.get_classification_widget(),
                            lambda event, group=exercise:
                            self._classification_onclick(event, group))
        self._bind_combobox(exercise.get_name_widget(),
                            lambda event, group=exercise:
                            self._exercise_name_onclick(event, group))

    def _initialize_exercise_comboboxes(self, exercise):
        exercise.set_classification_values(self.model.get_exercise_categories())
        exercise.set_name_values(self.model.get_exercise_names())
        exercise.set_link_values([])

    def _remove_exercise(self, event, block):
        block.remove_last_exercise()

    def _remove_block(self, event):
        self.view.remove_last_block()

    def _remove_all_blocks(self):
        while self.view.get_blocks():
            self.view.remove_last_block()

    def _classification_onclick(self, event, exercise):
        exercise.set_name_text('')
        exercise.set_link_text('')
        exercise.set_name_values(self.model.get_exercises_of_category(
                                            exercise.get_classification_text()))

    def _exercise_name_onclick(self, event, exercise):
        exercise.set_link_text('')
        exercise.set_link_values(self.model.get_exercise_video_links(
                                                    exercise.get_name_text()))

    def _view_onclick(self, event, exercise):
        webbrowser.open_new(exercise.get_link_text())

    def _clear_onclick(self, event, exercise):
        exercise.set_classification_text('')
        exercise.set_name_text('')
        exercise.set_sets_text(0)
        exercise.set_reps_text(0)
        exercise.set_intensity_text(0)
        exercise.set_link_text('')
        self._initialize_exercise_comboboxes(exercise)

    def _save_workout(self, event):
        filename = self.view.get_workout_name()
        with open(filename + '.csv', mode='w', newline='') as outfile:
            output_writer = csv.writer(outfile, delimiter=',')
            output_writer.writerow(['block number',
                                    'exercise number',
                                    'block name',
                                    'classification',
                                    'exercise name',
                                    'sets',
                                    'reps',
                                    'intensity',
                                    'link'])
            for block_number, block in enumerate(self.view.get_blocks(), start=1):
                for exercise_number, exercise in enumerate(block.get_exercises(), start=1):
                    output_writer.writerow([block_number,
                                            exercise_number,
                                            block.get_block_name(),
                                            exercise.get_classification_text(),
                                            exercise.get_name_text(),
                                            exercise.get_sets_text(),
                                            exercise.get_reps_text(),
                                            exercise.get_intensity_text(),
                                            exercise.get_link_text()])

    def _load_workout(self, event):
        self._remove_all_blocks()
        filename = self.view.get_workout_name()
        with open(filename + '.csv', 'r') as infile:
            data = csv.DictReader(infile, delimiter=',')
            current_block_num = 0
            current_block = None
            for row in data:
                if current_block_num != row['block number']:
                    current_block = self._add_block()
                    current_block.set_block_name(row['block name'])
                    current_block_num = row['block number']
                new_exercise = self._add_exercise(None, current_block)
                new_exercise.set_classification_text(row['classification'])
                new_exercise.set_name_text(row['exercise name'])
                new_exercise.set_sets_text(row['sets'])
                new_exercise.set_reps_text(row['reps'])
                new_exercise.set_intensity_text(row['intensity'])
                new_exercise.set_link_text(row['link'])

    def run(self):
        self.root.title('KELLEY\'S WORKOUT BUILDER')
        self.root.mainloop()
