import json
import datetime


class Note:
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return f"{self.id} - {self.title} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})\n{self.body}"


class NotesManager:
    def __init__(self):
        self.notes = []

    def load_notes(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for note_data in data:
                    note = Note(note_data['id'], note_data['title'], note_data['body'])
                    note.timestamp = datetime.datetime.strptime(note_data['timestamp'], '%Y-%m-%d %H:%M:%S')
                    self.notes.append(note)
        except FileNotFoundError:
            pass

    def save_notes(self, filename):
        with open(filename, "w") as f:
            data = []
            for note in self.notes:
                note_data = {
                    'id': note.id,
                    'title': note.title,
                    'body': note.body,
                    'timestamp': note.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
                data.append(note_data)
            json.dump(data, f)

    def list_notes(self):
        for note in self.notes:
            print(str(note))

    def add_note(self, title, body):
        id = 1
        if len(self.notes) > 0:
            id = self.notes[-1].id + 1
        note = Note(id, title, body)
        self.notes.append(note)
        return note

    def get_note_by_id(self, id):
        for note in self.notes:
            if note.id == id:
                return note
        return None

    def edit_note_by_id(self, id, title, body):
        note = self.get_note_by_id(id)
        if note is not None:
            note.title = title
            note.body = body
            note.timestamp = datetime.datetime.now()
            return note
        return None

    def delete_note_by_id(self, id):
        note = self.get_note_by_id(id)
        if note is not None:
            self.notes.remove(note)
            return True
        return False


notes_manager = NotesManager()
notes_manager.load_notes("notes.json")

while True:
    print("1. Примечания к списку")
    print("2. Добавить заметку")
    print("3. Изменить заметку")
    print("4. Удалить заметку")
    print("5. Выход")

    choice = input("Введите свой выбор: ")
    if choice == "1":
        notes_manager.list_notes()
    elif choice == "2":
        title = input("Введите название заметки: ")
        body = input("Введите текст заметки: ")
        note = notes_manager.add_note(title, body)
        print(f"Примечание добавлено: {str(note)}")
    elif choice == "3":
        id = int(input("Введите идентификатор заметки : "))
        title = input("Введите новое название заметки: ")
        body = input("Введите новое тело заметки: ")
        note = notes_manager.edit_note_by_id(id, title, body)
        if note is not None:
            print(f"Примечание изменено: {str(note)}")
        else:
            print("Примечание не найдено.")
    elif choice == "4":
        id = int(input("Введите идентификатор заметки: "))
        if notes_manager.delete_note_by_id(id):
            print("Примечание удалено.")
        else:
            print("Примечание не найдено.")
    elif choice == "5":
        notes_manager.save_notes("notes.json")
        break
    else:
        print("Неверный выбор.")
