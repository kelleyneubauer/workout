# KELLEY'S WORKOUT BUILDER

### Kelley Neubauer

Workout builder is a desktop application for building custom workouts with Tkinter

<img src="/img/workout_builder_create.gif">

---

**Features:**

- Dynamically add/remove exercises at runtime
- Save and load workouts in CSV format
- Populate comboboxes using JSON dataset
- Validates exercises by category selected
- Opens demo video link in web browser

<img src="/img/workout_builder_save_load.gif">

---

**How to run:**

1. Navigate to src folder folder using `cd src`
2. To run, type `python3 workout_builder.py`
3. Tkinter GUI window will automatically open
4. To end program, close the GUI window

**Save a workout:**
- input data as desired
- type `name` into 'Workout Name' field
- click save button
- workout will be saved as `name.csv` in same directory as program

**Load a workout:**
- type file name without .csv extension into 'Workout Name' field (e.g. `name.csv` should be entered as `name`)
- click load button

---

**CSV output format:**

example file included: `kelley_day_1.csv`
```
block number,exercise number,block name,classification,exercise name,sets,reps,intensity,link
1,1,block1 - lower body,Squat,Barbell Back Squat,4,10,85,https://youtu.be/chEiZVn0xbg
1,2,block1 - lower body,Explosive - Low,DB Squat Jump,4,5,85,https://youtu.be/39I1QNQDhy0
1,3,block1 - lower body,Mobility,Supine SL Drop w/ Ham Stretch,4,3e,0,https://youtu.be/CJ7k5IVJE0o
2,1,block2 - upper body,Horizontal Push,Barbell Bench Press,3,10,80,https://youtu.be/C7Te-IyY53o
2,2,block2 - upper body,Horizontal Pull,Band Face Pull,3,10,80,https://youtu.be/7bl5VFvgrfc
2,3,block2 - upper body,Prehab,Prone I-Y-T on Incline,3,10e,70,https://youtu.be/On3rx4h2eiQ
3,1,block3 - core,Core,Heavy St. Arm Crunch,3,20,65,https://youtu.be/TJDfI0Hk6q8
3,2,block3 - core,Core Rotation,Band 1/2 Kneeling Twist,3,10e,65,https://youtu.be/5Z9LXC1Qrj0

```

---

**JSON input format:**

dataset must be called `exercise_db.json`
the key must be called `exercises` may contain any number of exercises in the following format
```
{
	"exercises": {
		"Barbell Bench Press": {
			"exercise name": "Barbell Bench Press",
			"movement classifications": ["Horizontal Push"],
			"modality": ["Barbell"],
			"base exercise": "Bench Press",
			"level": "",
			"video links": ["https://youtu.be/C7Te-IyY53o", "https://youtu.be/oIirnwjG1Fw"],
			"reference links": [],
			"coaching & points of emphasis": "",
			"set up notes": ""
		},
		"Barbell Bent Row": {
			"exercise name": "Barbell Bent Row",
			"movement classifications": ["Horizontal Pull"],
			"modality": ["Barbell"],
			"base exercise": "",
			"level": "",
			"video links": ["https://youtu.be/lPZyycAdiwQ"],
			"reference links": [],
			"coaching & points of emphasis": "",
			"set up notes": ""
		}
	}
}
```

---

**To do:**
- [ ] clean up code smells
- [ ] add CRUD features
- [ ] figure out screen glitch when buttons are clicked
- [ ] verify elements are deleted when removed from screen
