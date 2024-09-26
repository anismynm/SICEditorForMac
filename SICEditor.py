## SICEditor For Mac
## made by anismynm

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QKeySequenceEdit
from PyQt5.QtCore import Qt

class SICAssemblyEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.srcfile_path = os.path.join(self.script_dir, 'SRCFILE')
        self.initUI()
        self.load_file()  # 프로그램 시작 시 SRCFILE 불러오기

    def initUI(self):
        self.setWindowTitle('SIC Editor (by anismynm)')
        self.setGeometry(100, 100, 500, 600)

        # 테이블 생성 (4열: Label, Operation, Operand, Comment)
        self.table = QTableWidget(self)
        self.table.installEventFilter(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Label', 'Operation', 'Operand', 'Comment'])

        # 버튼 생성
        self.btn_append = QPushButton('Append', self)
        self.btn_insert = QPushButton('Insert', self)
        self.btn_delete = QPushButton('Delete', self)
        self.btn_clear = QPushButton('Clear', self)
        self.btn_save = QPushButton('Save', self)
        
        # 버튼 동작 연결
        self.btn_append.clicked.connect(self.append_row)
        self.btn_insert.clicked.connect(self.insert_row)
        self.btn_delete.clicked.connect(self.delete_row)
        self.btn_clear.clicked.connect(self.clear_table)
        self.btn_save.clicked.connect(self.save_file)

        # 레이아웃 설정
        layout = QVBoxLayout()

        row1_layout = QHBoxLayout()
        row1_layout.addWidget(self.btn_append)
        row1_layout.addWidget(self.btn_insert)

        row2_layout = QHBoxLayout()
        row2_layout.addWidget(self.btn_delete)
        row2_layout.addWidget(self.btn_clear)

        row3_layout = QHBoxLayout()
        row3_layout.addWidget(self.btn_save)

        layout.addWidget(self.table)
        layout.addLayout(row1_layout)
        layout.addLayout(row2_layout)  
        layout.addLayout(row3_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def append_row(self):
        # 테이블 마지막에 행 추가
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def insert_row(self):
        # 현재 선택된 위치에 행 추가
        row_position = self.table.currentRow()
        if row_position == -1:
            row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def delete_row(self):
        # 선택된 행 삭제
        row_position = self.table.currentRow()
        if row_position != -1:
            self.table.removeRow(row_position)

    def clear_table(self):
        # 테이블 초기화
        self.table.setRowCount(0)

    def load_file(self):
        # SRCFILE 파일을 열고 데이터를 테이블에 로드
        try:
            with open(self.srcfile_path, 'r') as file:
                lines = file.readlines()
                self.table.setRowCount(len(lines))  # 파일의 줄 수만큼 행 생성
                for row, line in enumerate(lines):
                    # 라인에서 각 부분을 슬라이싱하여 추출
                    label = line[0:7].strip()      # 1-8 Label
                    operation = line[9:14].strip() # 10-15 Operation code
                    operand = line[17:34].strip()  # 18-35 Operand
                    comment = line[35:65].strip()  # 36-66 Comment

                    # 테이블에 각각의 값을 삽입
                    self.table.setItem(row, 0, QTableWidgetItem(label))
                    self.table.setItem(row, 1, QTableWidgetItem(operation))
                    self.table.setItem(row, 2, QTableWidgetItem(operand))
                    self.table.setItem(row, 3, QTableWidgetItem(comment))
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "SRCFILE not found! Starting with a blank table.")

    def save_file(self):
        # SRCFILE 파일에 테이블 데이터를 저장
        try:
            with open(self.srcfile_path, 'w') as file:
                for row in range(self.table.rowCount()):
                    label = self.table.item(row, 0).text() if self.table.item(row, 0) else ''
                    operation = self.table.item(row, 1).text() if self.table.item(row, 1) else ''
                    operand = self.table.item(row, 2).text() if self.table.item(row, 2) else ''
                    comment = self.table.item(row, 3).text() if self.table.item(row, 3) else ''
                    
                    # SIC Assembly 포맷에 맞게 저장
                    formatted_line = f"{label.ljust(8)} {operation.ljust(6)}  {operand.ljust(18)}{comment.ljust(30)}\r\n"
                    file.write(formatted_line)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error saving file: {str(e)}")

    def closeEvent(self, event):
        # 창이 닫힐 때 SRCFILE 자동 저장
        self.save_file()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = SICAssemblyEditor()
    editor.show()
    sys.exit(app.exec_())
