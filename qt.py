import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import Qt

from open_mp4_for_qt import generate_video


class DragAndDropWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.label1 = QLabel('Видео', self)
        self.setup_label(self.label1)

        self.label2 = QLabel('Данные об опасных зонах', self)
        self.setup_label(self.label2)

        self.button_start = QPushButton('Начать', self)
        self.button_start.clicked.connect(self.start_processing)
        self.button_start.setStyleSheet('background-color: #4CAF50; color: white; padding: 10px;')

        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.button_start)

        self.setWindowTitle('Drag and Drop')
        self.setGeometry(300, 300, 400, 200)
        self.setStyleSheet('background-color: #333; color: white;')
        self.show()

        self.selected_file_path1 = None
        self.selected_file_path2 = None

    def setup_label(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setAcceptDrops(True)
        label.setStyleSheet('border: 2px dashed #aaa; padding: 20px; background-color: #444; color: #ccc;')
        label.dragEnterEvent = self.drag_enter_event
        label.dropEvent = self.drop_event
        label.mousePressEvent = lambda event: self.select_file(event, label)

    def drag_enter_event(self, e):
        e.accept()

    def drop_event(self, e):
        mime_data = e.mimeData()

        if mime_data.hasUrls():
            for url in mime_data.urls():
                file_path = url.toLocalFile()

                if self.sender() == self.label1:
                    self.selected_file_path1 = file_path
                    self.label1.setText(f'Выбран файл: {self.selected_file_path1}')
                elif self.sender() == self.label2:
                    self.selected_file_path2 = file_path
                    self.label2.setText(f'Выбран файл: {self.selected_file_path2}')

                print(f'Добавлен файл: {file_path}')

    def select_file(self, event, label):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)

        selected_file, _ = file_dialog.getOpenFileName(self, "Выберите файл")
        if selected_file:
            if label == self.label1:
                self.selected_file_path1 = selected_file
                self.label1.setText(f'Видео: {self.selected_file_path1}')
            elif label == self.label2:
                self.selected_file_path2 = selected_file
                self.label2.setText(f'Данные о опасных зонах: {self.selected_file_path2}')

    def start_processing(self):
        generate_video(self.selected_file_path1, self.selected_file_path2)
        # if self.selected_file_path1==None or self.selected_file_path2==None:
        #   print('123')
        # else:pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DragAndDropWidget()
    sys.exit(app.exec_())
