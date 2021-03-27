#!usr/bin/env python3

import tkinter as tk
from tkinter import ttk


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
            while last_block._exercises:
                last_block.remove_last_exercise()
            last_block.destroy_widgets()

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
        while self._exercises:
            self.remove_last_exercise()
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
