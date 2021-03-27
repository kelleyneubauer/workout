#!usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import json
import webbrowser
import csv


class Model:
    def __init__(self):
        self._data = self._read_json('exercise_db.json')
        self._exercises_by_category = self._sort_exercises_by_category(self._data)

    def _read_json(self, file_name):
        with open(file_name, 'r') as infile:
            return json.load(infile)

    def _sort_exercises_by_category(self, data):
        data = self._sort_exercises_into_categories(data)
        data = self._sort_exercises_within_categories(data)
        return data

    def _sort_exercises_into_categories(self, data):
        exercise_by_cat = {}
        for exercise in data['exercises']:
            for category in data['exercises'][exercise]['movement classifications']:
                if category not in exercise_by_cat:
                    exercise_by_cat[category] = [exercise]
                else:
                    exercise_by_cat[category].append(exercise)
        return exercise_by_cat

    def _sort_exercises_within_categories(self, data):
        for key in data:
            data[key] = sorted(data[key])
        return data

    def get_exercise_categories(self):
        return sorted(list(self._exercises_by_category.keys()))

    def get_exercise_names(self):
        return sorted(list(self._data['exercises'].keys()))

    def get_exercises_of_category(self, category):
        return self._exercises_by_category[category]

    def get_exercise_video_links(self, exercise_name):
        return self._data['exercises'][exercise_name]['video links']


class View:
    def __init__(self, master):
        self._frm = tk.Frame(master=master, height=200, width=200)
        self._frm.grid(row=0, column=0)
        master.columnconfigure(0, weight=1)

        self._frm_header = tk.Frame(master=self._frm)
        self._frm_header.grid(row=0, column=0, sticky='w')
        self._lbl_header = tk.Label(master=self._frm_header, text='Workout Name: ',  width=12, anchor='w')
        self._lbl_header.grid(row=0, column=0, sticky='w')
        self._ent_header_name = tk.Entry(master=self._frm_header)
        self._ent_header_name.grid(row=0, column=1, sticky='w')

        self._btn_remove_block = tk.Button(master=self._frm_header, text='-', width=1)
        self._btn_remove_block.grid(row=0, column=2)
        self._btn_add_block = tk.Button(master=self._frm_header, text='+', width=1)
        self._btn_add_block.grid(row=0, column=3)

        self._btn_save = tk.Button(master=self._frm_header, text='save', width=3)
        self._btn_save.grid(row=0, column=4, padx=(500, 0))
        self._btn_load = tk.Button(master=self._frm_header, text='load', width=3)
        self._btn_load.grid(row=0, column=5)

        self._exercise_blocks = []

    def add_block(self, quantity=1, exercises=0):
        for x in range(0, quantity):
            self._exercise_blocks.append(ExerciseBlock(self._frm, len(self._exercise_blocks) + 1))
            if exercises:
                self._exercise_blocks[len(self._exercise_blocks) - 1].add_exercise(exercises)

    def remove_last_block(self):
        if self._exercise_blocks:
            last_block = self._exercise_blocks.pop()
            last_block.destroy_widgets()
            # for widget in last_block.get_frame().winfo_children():
            #     widget.destroy()
            # last_block.get_frame().grid_forget()
            # last_block.get_frame().destroy()

    def get_last_block(self):
        if self._exercise_blocks:
            return self._exercise_blocks[-1]
        return None

    def get_add_block_widget(self):
        return self._btn_add_block

    def get_remove_block_widget(self):
        return self._btn_remove_block

    def get_save_widget(self):
        return self._btn_save

    def get_load_widget(self):
        return self._btn_load

    def get_workout_name(self):
        return self._ent_header_name.get()

    def get_blocks(self):
        return self._exercise_blocks


class ExerciseBlock:
    labels = [('classification', 22), ('exercise name', 37), ('sets', 7), ('reps', 7), ('intensity', 7), ('video link', 22)]

    def __init__(self, master, block_num):
        self._frm = tk.Frame(master=master)
        self._frm.grid(row=block_num, column=0, sticky='w', pady=(20, 0))

        self._frm_header = tk.Frame(master=self._frm)
        self._frm_header.grid(row=0, column=0, sticky='w')

        self._lbl_block_name = tk.Label(master=self._frm_header, text='Block Name: ', width=12, anchor='w')
        self._lbl_block_name.grid(row=0, column=0, sticky='w')
        
        self._ent_block_name = tk.Entry(master=self._frm_header)
        self._ent_block_name.grid(row=0, column=1, sticky='w')
        
        self._btn_remove_exercise = tk.Button(master=self._frm_header, text='-', width=1)
        self._btn_remove_exercise.grid(row=0, column=2)
        
        self._btn_add_exercise = tk.Button(master=self._frm_header, text='+', width=1)
        self._btn_add_exercise.grid(row=0, column=3)

        self._frm_body = tk.Frame(master=self._frm)
        self._frm_body.grid(row=1, column=0, sticky='w')

        self._frm_body_labels = tk.Frame(master=self._frm_body)
        self._frm_body_labels.grid(row=0, column=0, sticky='w')

        for i in range(len(ExerciseBlock.labels)):
            lbl = tk.Label(master=self._frm_body_labels, text=ExerciseBlock.labels[i][0], width=ExerciseBlock.labels[i][1], anchor='w')
            lbl.grid(row=0, column=i, sticky='w', padx=(0, 3))

        self._exercises = []

    def destroy_widgets(self):
        for exercise in self._exercises:
            exercise.destroy_widgets()

        for frame in self._frm.winfo_children():
            for widget in frame.winfo_children():
                widget.grid_forget()
                widget.destroy()
            frame.grid_forget()
            frame.destroy()
        self._frm.grid_forget()
        self._frm.destroy()

    def add_exercise(self, quantity=1):
        for x in range(0, quantity):
            self._exercises.append(Exercise(self._frm_body, len(self._exercises) + 1))

    def remove_last_exercise(self):
        if self._exercises:
            last_exercise = self._exercises.pop()
            last_exercise.destroy_widgets()

    def get_frame(self):
        return self._frm

    def get_exercises(self):
        return self._exercises

    def get_last_exercise(self):
        if self._exercises:
            return self._exercises[-1]
        return None

    def get_add_exercise_widget(self):
        return self._btn_add_exercise

    def get_remove_exercise_widget(self):
        return self._btn_remove_exercise

    def get_block_name(self):
        return self._ent_block_name.get()

    def set_block_name(self, value):
        self._ent_block_name.delete(0, 'end')
        self._ent_block_name.insert(0, value)


class Exercise:
    def __init__(self, master, exercise_num):
        self._frm = tk.Frame(master=master)
        self._frm.grid(row=exercise_num, column=0, sticky='w')

        self._cmb_classification = ttk.Combobox(master=self._frm, width=20)
        self._cmb_classification.grid(row=0, column=0, sticky='w')

        self._cmb_exercise_name = ttk.Combobox(master=self._frm, width=35)
        self._cmb_exercise_name.grid(row=0, column=1, sticky='w')

        self._spn_sets = tk.Spinbox(master=self._frm, from_=0, to=99999, width=5)
        self._spn_sets.grid(row=0, column=2, sticky='w')

        self._spn_reps = tk.Spinbox(master=self._frm, from_=0, to=99999, width=5)
        self._spn_reps.grid(row=0, column=3)

        self._spn_intensity = tk.Spinbox(master=self._frm, from_=0, to=100, width=5)
        self._spn_intensity.grid(row=0, column=4)

        self._cmb_video_link = ttk.Combobox(master=self._frm, width=20)
        self._cmb_video_link.grid(row=0, column=5, sticky='w')

        self._btn_view_link = tk.Button(master=self._frm, text='view')
        self._btn_view_link.grid(row=0, column=6, sticky='w')

        self._btn_clear = tk.Button(master=self._frm, text='clear')
        self._btn_clear.grid(row=0, column=7, sticky='w')

    def destroy_widgets(self):
        for widget in self._frm.winfo_children():
            widget.grid_forget()
            widget.destroy()
        self._frm.grid_forget()
        self._frm.destroy()

    def get_classification_text(self):
        return self._cmb_classification.get()

    def get_classification_widget(self):
        return self._cmb_classification

    def get_name_text(self):
        return self._cmb_exercise_name.get()

    def get_name_widget(self):
        return self._cmb_exercise_name

    def get_sets_text(self):
        return self._spn_sets.get()

    def get_reps_text(self):
        return self._spn_reps.get()

    def get_intensity_text(self):
        return self._spn_intensity.get()

    def get_link_text(self):
        return self._cmb_video_link.get()

    def get_link_widget(self):
        return self._cmb_video_link

    def get_view_link_widget(self):
        return self._btn_view_link

    def get_clear_widget(self):
        return self._btn_clear

    def set_classification_text(self, value):
        self._cmb_classification.set(value)

    def set_classification_values(self, values):
        self._cmb_classification['values'] = values

    def set_name_text(self, value):
        self._cmb_exercise_name.set(value)

    def set_name_values(self, values):
        self._cmb_exercise_name['values'] = values

    def set_sets_text(self, value):
        self._spn_sets.delete(0, 'end')
        self._spn_sets.insert(0, value)

    def set_reps_text(self, value):
        self._spn_reps.delete(0, 'end')
        self._spn_reps.insert(0, value)

    def set_intensity_text(self, value):
        self._spn_intensity.delete(0, 'end')
        self._spn_intensity.insert(0, value)

    def set_link_text(self, value):
        self._cmb_video_link.set(value)

    def set_link_values(self, values):
        self._cmb_video_link['values'] = values
        self._show_first_combo_value(self._cmb_video_link)

    def _show_first_combo_value(self, combobox):
        if combobox['values']:
            combobox.current(0)


class Controller:
    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.view = View(self.root)
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
            last_block = self.view.get_last_block()
            self._remove_all_exercises_in_block(last_block)
            self.view._remove_last_block()

        for block in self.view.exercise_blocks:
            self._remove_all_exercises_in_block(block)
        while self.view.exercise_blocks:
            self.view.remove_last_block()

    def _remove_all_exercises_in_block(self, block):
        while block.get_exercises():
            block.remove_last_exercise()

    def _classification_onclick(self, event, exercise):
        exercise.set_name_text('')
        exercise.set_link_text('')
        exercise.set_name_values(self.model.get_exercises_of_category(exercise.get_classification_text()))

    def _exercise_name_onclick(self, event, exercise):
        exercise.set_link_text('')
        exercise.set_link_values(self.model.get_exercise_video_links(exercise.get_name_text()))

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


if __name__ == '__main__':
    controller = Controller()
    controller.run()
