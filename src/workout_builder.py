#!usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import json
import webbrowser
import csv


class Model:
    def __init__(self):
        self.data = self._read_json('exercise_db.json')
        self.exercises_by_category = self._sort_exercises_by_category(self.data)

    def _read_json(self, file_name):
        with open(file_name, 'r') as input:
            return json.load(input)

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
        return sorted(list(self.exercises_by_category.keys()))

    def get_exercise_names(self):
        return sorted(list(self.data['exercises'].keys()))

    def get_exercises_of_category(self, category):
        return self.exercises_by_category[category]

    def get_exercise_video_links(self, exercise_name):
        return self.data['exercises'][exercise_name]['video links']


class View:
    def __init__(self, master):
        self.frm = tk.Frame(master=master, height=200, width=200)
        self.frm.grid(row=0, column=0)
        master.columnconfigure(0, weight=1)

        # header frame
        self.frm_header = tk.Frame(master=self.frm)
        self.frm_header.grid(row=0, column=0, sticky='w')
        self.lbl_header = tk.Label(master=self.frm_header, text='Workout Name: ',  width=12, anchor='w')
        self.lbl_header.grid(row=0, column=0, sticky='w')
        self.ent_header_name = tk.Entry(master=self.frm_header)
        self.ent_header_name.grid(row=0, column=1, sticky='w')

        self.btn_remove_block = tk.Button(master=self.frm_header, text='-', width=1)
        self.btn_remove_block.grid(row=0, column=2)
        self.btn_add_block = tk.Button(master=self.frm_header, text='+', width=1)
        self.btn_add_block.grid(row=0, column=3)

        self.btn_save = tk.Button(master=self.frm_header, text='save', width=3)
        self.btn_save.grid(row=0, column=4, padx=(500, 0))
        self.btn_load = tk.Button(master=self.frm_header, text='load', width=3)
        self.btn_load.grid(row=0, column=5)

        self.exercise_blocks = []

    def add_block(self, quantity=1, exercises=0):
        for x in range(0, quantity):
            self.exercise_blocks.append(ExerciseBlock(self.frm, len(self.exercise_blocks) + 1))
            if exercises:
                self.exercise_blocks[len(self.exercise_blocks) - 1].add_exercise(exercises)

    def remove_last_block(self):
        # last_block = self.exercise_blocks[len(self.exercise_blocks) - 1]
        if self.exercise_blocks:
            last_block = self.exercise_blocks.pop()
            for widget in last_block.frm.winfo_children():
                widget.destroy()
            last_block.frm.grid_forget()
            last_block.frm.destroy()

    def get_last_block(self):
        if self.exercise_blocks:
            return self.exercise_blocks[-1]
        return None


class ExerciseBlock:
    labels = [('classification', 22), ('exercise name', 37), ('sets', 7), ('reps', 7), ('intensity', 7), ('video link', 22)]

    def __init__(self, master, block_num):

        self.frm = tk.Frame(master=master)
        self.frm.grid(row=block_num, column=0, sticky='w', pady=(20, 0))

        self.frm_header = tk.Frame(master=self.frm)
        self.frm_header.grid(row=0, column=0, sticky='w')

        self.lbl_block_name = tk.Label(master=self.frm_header, text='Block Name: ', width=12, anchor='w')
        self.lbl_block_name.grid(row=0, column=0, sticky='w')
        self.ent_block_name = tk.Entry(master=self.frm_header)
        self.ent_block_name.grid(row=0, column=1, sticky='w')
        self.btn_remove_exercise = tk.Button(master=self.frm_header, text='-', width=1)
        self.btn_remove_exercise.grid(row=0, column=2)
        self.btn_add_exercise = tk.Button(master=self.frm_header, text='+', width=1)
        self.btn_add_exercise.grid(row=0, column=3)

        self.frm_body = tk.Frame(master=self.frm)
        self.frm_body.grid(row=1, column=0, sticky='w')

        self.frm_body_labels = tk.Frame(master=self.frm_body)
        self.frm_body_labels.grid(row=0, column=0, sticky='w')

        for i in range(len(ExerciseBlock.labels)):
            lbl = tk.Label(master=self.frm_body_labels, text=ExerciseBlock.labels[i][0], width=ExerciseBlock.labels[i][1], anchor='w')
            lbl.grid(row=0, column=i, sticky='w', padx=(0, 3))

        self.exercises = []

    def add_exercise(self, quantity=1):
        for x in range(0, quantity):
            self.exercises.append(Exercise(self.frm_body, len(self.exercises) + 1))

    def remove_last_exercise(self):
        if self.exercises:
            last_exercise = self.exercises.pop()
            for widget in last_exercise.frm.winfo_children():
                widget.destroy()
            last_exercise.frm.grid_forget()
            last_exercise.frm.destroy()

    def get_last_exercise(self):
        if self.exercises:
            return self.exercises[-1]
        return None


class Exercise:
    def __init__(self, master, exercise_num):

        self.frm = tk.Frame(master=master)
        self.frm.grid(row=exercise_num, column=0, sticky='w')

        self.cmb_classification = ttk.Combobox(master=self.frm, width=20)
        self.cmb_classification.grid(row=0, column=0, sticky='w')

        self.cmb_exercise_name = ttk.Combobox(master=self.frm, width=35)
        self.cmb_exercise_name.grid(row=0, column=1, sticky='w')

        self.spn_sets = tk.Spinbox(master=self.frm, from_=0, to=99999, width=5)
        self.spn_sets.grid(row=0, column=2)

        self.spn_reps = tk.Spinbox(master=self.frm, from_=0, to=99999, width=5)
        self.spn_reps.grid(row=0, column=3)

        self.spn_intensity = tk.Spinbox(master=self.frm, from_=0, to=100, width=5)
        self.spn_intensity.grid(row=0, column=4)

        self.cmb_video_link = ttk.Combobox(master=self.frm, width=20)
        self.cmb_video_link.grid(row=0, column=5, sticky='w')

        self.btn_view_link = tk.Button(master=self.frm, text='view')
        self.btn_view_link.grid(row=0, column=6, sticky='w')

        self.btn_clear = tk.Button(master=self.frm, text='clear')
        self.btn_clear.grid(row=0, column=7, sticky='w')

    def get_classification(self):
        return self.cmb_classification.get()

    def get_name(self):
        return self.cmb_exercise_name.get()

    def get_sets(self):
        return self.spn_sets.get()

    def get_reps(self):
        return self.spn_reps.get()

    def get_intensity(self):
        return self.spn_intensity.get()

    def get_link(self):
        return self.cmb_video_link.get()

    def set_classification_text(self, value):
        self.cmb_classification.set(value)

    def set_classification_values(self, values):
        self.cmb_classification['values'] = values

    def set_name_text(self, value):
        self.cmb_exercise_name.set(value)

    def set_name_values(self, values):
        self.cmb_exercise_name['values'] = values

    def set_sets_text(self, value):
        self.spn_sets.delete(0, 'end')
        self.spn_sets.insert(0, value)

    def set_reps_text(self, value):
        self.spn_reps.delete(0, 'end')
        self.spn_reps.insert(0, value)

    def set_intensity_text(self, value):
        self.spn_intensity.delete(0, 'end')
        self.spn_intensity.insert(0, value)

    def set_link_text(self, value):
        self.cmb_video_link.set(value)

    def set_link_values(self, values):
        self.cmb_video_link['values'] = values
        self._show_first_combo_value(self.cmb_video_link)

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
        self._bind_button(self.view.btn_save, self._save_workout)
        self._bind_button(self.view.btn_load, self._load_workout)
        self._bind_button(self.view.btn_add_block, self._add_block)
        self._bind_button(self.view.btn_remove_block, self._remove_block)

    def _bind_button(self, button, handler):
        button.bind('<Button>', handler)

    def _bind_combobox(self, combobox, handler):
        combobox.bind('<<ComboboxSelected>>', handler)

    def _add_block(self, event=None):
        self.view.add_block()
        new_block = self.view.get_last_block()
        self._bind_block_events(new_block)

    def _bind_block_events(self, block):
        self._bind_button(block.btn_add_exercise,
                          lambda event, group=block:
                          self._add_exercise(event, group))
        self._bind_button(block.btn_remove_exercise,
                          lambda event, group=block:
                          self._remove_exercise(event, group))

    def _add_exercise(self, event, block):
        block.add_exercise()
        new_exercise = block.get_last_exercise()
        self._bind_exercise_events(new_exercise)
        self._initialize_exercise_comboboxes(new_exercise)

    def _bind_exercise_events(self, exercise):
        self._bind_button(exercise.btn_clear,
                          lambda event, group=exercise:
                          self._clear_onclick(event, group))
        self._bind_button(exercise.btn_view_link,
                          lambda event, group=exercise:
                          self._view_onclick(event, group))
        self._bind_combobox(exercise.cmb_classification,
                            lambda event, group=exercise:
                            self._classification_onclick(event, group))
        self._bind_combobox(exercise.cmb_exercise_name,
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
        for block in self.view.exercise_blocks:
            self._remove_all_exercises_in_block(block)
        while self.view.exercise_blocks:
            self.view.remove_last_block()

    def _remove_all_exercises_in_block(self, block):
        while block.exercises:
            block.remove_last_exercise()

    def _classification_onclick(self, event, exercise):
        exercise.set_name_text('')
        exercise.set_link_text('')
        exercise.set_name_values(self.model.get_exercises_of_category(exercise.cmb_classification.get()))

    def _exercise_name_onclick(self, event, exercise):
        exercise.set_link_text('')
        exercise.set_link_values(self.model.get_exercise_video_links(exercise.cmb_exercise_name.get()))

    def _view_onclick(self, event, exercise):
        webbrowser.open_new(exercise.get_link())

    def _clear_onclick(self, event, exercise):
        exercise.set_classification_text('')
        exercise.set_name_text('')
        exercise.set_sets_text(0)
        exercise.set_reps_text(0)
        exercise.set_intensity_text(0)
        exercise.set_link_text('')
        self._initialize_exercise_comboboxes(exercise)





    def _save_workout(self, event):
        filename = self.view.ent_header_name.get()
        with open(filename + '.csv', mode='w', newline='') as output:
            output_writer = csv.writer(output, delimiter=',')
            output_writer.writerow(['block number', 'exercise number', 'block name', 'classification', 'exercise name', 'sets', 'reps', 'intensity', 'link'])
            block_number = 0
            for block in self.view.exercise_blocks:
                block_name = block.ent_block_name.get()
                block_number += 1
                exercise_number = 0
                for exercise in block.exercises:
                    exercise_number += 1
                    classification = exercise.cmb_classification.get()
                    exercise_name = exercise.cmb_exercise_name.get()
                    sets = exercise.spn_sets.get()
                    reps = exercise.spn_reps.get()
                    intensity = exercise.spn_intensity.get()
                    link = exercise.cmb_video_link.get()
                    output_writer.writerow([block_number, exercise_number, block_name, classification, exercise_name, sets, reps, intensity, link])

    def _load_workout(self, event):
        self._remove_all_blocks()

        filename = self.view.ent_header_name.get()
        data = []
        with open(filename + '.csv', 'r') as input:
            data = csv.reader(input, delimiter=',')
            next(data)
            data = list(data)
        # put the data into a dict where the key is a (block #, block name) and the value is a list of exercises
        data_dict = {}
        for row in data:
            if (row[0], row[2]) not in data_dict:
                data_dict[(row[0], row[2])] = [row]
            else:
                data_dict[(row[0], row[2])].append(row)

        for key in data_dict:
            self._add_block()
            new_block = self.view.exercise_blocks[-1]
            new_block.ent_block_name.delete(0, 'end')
            new_block.ent_block_name.insert(0, key[1])
            for item in data_dict[key]:
                self._add_exercise(None, new_block)
                new_exercise = new_block.exercises[-1]

                new_exercise.cmb_classification.set(item[3])
                new_exercise.cmb_exercise_name.set(item[4])
                new_exercise.spn_sets.delete(0, 'end')
                new_exercise.spn_sets.insert(0, item[5])
                new_exercise.spn_reps.delete(0, 'end')
                new_exercise.spn_reps.insert(0, item[6])
                new_exercise.spn_intensity.delete(0, 'end')
                new_exercise.spn_intensity.insert(0, item[7])
                new_exercise.cmb_video_link.set(item[8])

    def run(self):
        self.root.title('KELLEY\'S WORKOUT BUILDER')
        self.root.mainloop()


if __name__ == '__main__':
    controller = Controller()
    controller.run()
