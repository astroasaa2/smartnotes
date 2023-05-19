from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json

app = QApplication([])
notes = []

notes_win = QWidget()
notes_win.setWindowTitle("Розумні замітки")
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel("Список заміток")

button_note_create = QPushButton("Створити замітку")
button_note_del = QPushButton("Видалити замітку")
button_note_save = QPushButton("Зберегти замітку")

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()

button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки за тегом')

list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)

# Нозву нової замітки
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати замітку", "Назва замітки:")
    if ok and note_name != "":
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        print(notes)
        with open(str(len(notes) - 1) + ".txt", "w") as file:
            file.write(note[0] + '\n')


def show_note():
    if list_notes.selectedItems():
        index = list_notes.currentRow()
        if 0 <= index < len(notes):
            note = notes[index]
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

def save_notes():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def del_note():
    if list_notes.selectedItems():
        index = list_notes.row(list_notes.selectedItems()[0])
        del notes[index]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        for note in notes:
            list_notes.addItem(note[0])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
            print(notes)
    else:
        print("Замітка для видалення не обрана!")

def add_tag():
    if list_notes.selectedItems():
        selected_item = list_notes.selectedItems()[0]
        note_name = selected_item.text()
        for note in notes:
            if note[0] == note_name:
                tag = field_tag.text()
                if tag not in note[2]:
                    note[2].append(tag)
                    list_tags.addItem(tag)
                    field_tag.clear()
                    with open("notes_data.json", "w") as file:
                        json.dump(notes, file, sort_keys=True, ensure_ascii=False)
                    print(notes)
                    break
        else:
            print("Нотатка для додавання не знайдена!")
    else:
        print("Нотатка для додавання не обрана!")

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        note_key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes_list = [note[0] for note in notes]
        note_index = notes_list.index(note_key)
        if tag in notes[note_index][2]:
            notes[note_index][2].remove(tag)
            list_tags.clear()
            list_tags.addItems(notes[note_index][2])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Нотатка або тег для видалення не обрані!")

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки за тегом" and tag:
        notes_filtered = [note[0] for note in notes if tag in note[2]]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems([note[0] for note in notes])
        button_tag_search.setText("Шукати замітки за тегом")
    else:
        pass

button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_notes)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

notes_win.show()

name = 0
note = []
while True:
    filename = str(name) + ".txt"
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.replace('\n', '')
                note.append(line)
        if len(note) >= 3:  
            tags = note[2].split(' ')
            note[2] = tags
            notes.append(note)
        note = []
        name += 1
    except IOError:
        break

for note in notes:
    list_notes.addItem(note[0])

app.exec_()

