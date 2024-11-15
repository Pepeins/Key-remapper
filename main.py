import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import keyboard

key_mappings = {}
creator_name = "Creador: Wesk"
version = "v0.0.3.1"

settings = QtCore.QSettings("Key Remapper", "Key Remaps")

def save_remaps():
    settings.clear()
    for key1, key2 in key_mappings.items():
        settings.setValue(key1, key2)

def load_remaps():
    for key in settings.allKeys():
        key_mappings[key] = settings.value(key)

def set_key_remap(key1, key2):
    key_mappings[key1] = key2
    key_mappings[key2] = key1

def remove_key_remap(key1):
    key2 = key_mappings.get(key1)
    if key2:
        del key_mappings[key1]
        del key_mappings[key2]

def remap_keys():
    keyboard.hook(lambda event: handle_key_press(event))

def handle_key_press(event):
    if event.event_type == keyboard.KEY_DOWN:
        key1 = event.name.lower()
        if key1 in key_mappings:
            key2 = key_mappings[key1]
            keyboard.press_and_release(key2)
            event.suppress()

class KeyRemapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.changes_unsaved = False
        self.initUI()
        load_remaps()
        remap_keys()

    def initUI(self):
        self.setWindowTitle('Key Remapper')
        self.setGeometry(100, 100, 400, 550)

        self.setStyleSheet("""
            QWidget {
                background-color: #2B2B2B;
                color: #E0E0E0;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #404040;
                color: #FFFFFF;
                padding: 8px;
                border: 2px solid #5B5B5B;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #5B8DFF;
                color: #FFFFFF;
                padding: 8px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A7AC7;
            }
            QPushButton:pressed {
                background-color: #375A94;
            }
            QListWidget {
                background-color: #404040;
                color: #E0E0E0;
                border: 2px solid #5B5B5B;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #5B8DFF;
                color: #FFFFFF;
            }
            QLabel {
                color: #5B8DFF;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            #creatorLabel {
                color: #A0A0A0;
                font-size: 12px;
                font-style: italic;
                margin-top: 15px;
            }
        """)

        self.layout = QtWidgets.QVBoxLayout()

        self.remap_label = QtWidgets.QLabel('Active Remaps')
        self.layout.addWidget(self.remap_label)

        self.remap_list = QtWidgets.QListWidget()
        self.update_remap_list()
        self.layout.addWidget(self.remap_list)

        self.key1_input = QtWidgets.QLineEdit(self)
        self.key1_input.setPlaceholderText('bind 1')
        self.layout.addWidget(self.key1_input)

        self.key2_input = QtWidgets.QLineEdit(self)
        self.key2_input.setPlaceholderText('bind 2')
        self.layout.addWidget(self.key2_input)

        self.add_button = QtWidgets.QPushButton('Add Remapping', self)
        self.add_button.clicked.connect(self.add_remap)
        self.layout.addWidget(self.add_button)

        self.remove_button = QtWidgets.QPushButton('Delete Selected Remapping', self)
        self.remove_button.clicked.connect(self.remove_selected_remap)
        self.layout.addWidget(self.remove_button)

        self.save_button = QtWidgets.QPushButton('Save and close', self)
        self.save_button.clicked.connect(self.save_and_exit)
        self.layout.addWidget(self.save_button)

        self.creator_label = QtWidgets.QLabel(f"{creator_name} | {version}")
        self.creator_label.setObjectName("creatorLabel")
        self.creator_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.creator_label)

        self.setLayout(self.layout)

    def add_remap(self):
        key1 = self.key1_input.text().strip().lower()
        key2 = self.key2_input.text().strip().lower()

        if not key1 or not key2:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Enter both keys.')
            return
        if key1 == key2 or key1 in key_mappings or key2 in key_mappings:
            QtWidgets.QMessageBox.warning(self, 'Error', 'The keys are the same or are already in a remapping.')
            return

        set_key_remap(key1, key2)
        self.update_remap_list()
        self.key1_input.clear()
        self.key2_input.clear()
        self.changes_unsaved = True

    def remove_selected_remap(self):
        selected_item = self.remap_list.currentItem()
        if selected_item:
            remap_text = selected_item.text()
            key1, key2 = remap_text.split(' ↔ ')
            remove_key_remap(key1)
            self.update_remap_list()
            self.changes_unsaved = True
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Select remapping to delete.')

    def update_remap_list(self):
        self.remap_list.clear()
        for k1, k2 in key_mappings.items():
            if k1 < k2:
                self.remap_list.addItem(f"{k1} ↔ {k2}")

    def save_and_exit(self):
        save_remaps()
        QtWidgets.QMessageBox.information(self, 'Saved', 'Successfully saved remappings.')
        self.changes_unsaved = False
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    remap_app = KeyRemapApp()
    remap_app.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
