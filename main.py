import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QComboBox, QGridLayout, QPlainTextEdit, QMessageBox, QApplication, \
    QCheckBox, QHBoxLayout
import sys
import keyboard
import pyperclip
from global_hotkeys import stop_checking_hotkeys, start_checking_hotkeys, register_hotkeys


class MainUI(QWidget):

    def __init__(self):
        super().__init__()
        self.stopKey = None
        self.startKey = None
        self.indentation = None
        self.endLines = None
        self.lineDelay = None
        self.setFixedWidth(700)
        self.setFixedHeight(500)
        self.delay = None
        self.key = None
        self.clipBoard = None
        self.autoFormat = None
        self.format = False
        self.clip = False
        self.stop = False
        self.setWindowIcon(QIcon('python.ico'))
        self.setWindowTitle("Auto Code Typer ( By M.Nagendra )")
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.autoFormatWidget()
        self.keyLabel = QLabel(
            "Shortcut Key=>\tctrl + shift + " +
            self.startKey.currentText() + "\tStop: " +
            self.stopKey.currentText())
        self.grid.addWidget(self.keyLabel, 0, 1, 1, 2)
        title1 = QLabel("\tText :")
        title1.setAlignment(Qt.AlignTop)
        self.grid.addWidget(title1, 1, 0)
        self.txtArea = QPlainTextEdit()
        self.txtArea.setPlainText("Automate Text/Code Typing with Auto Code Typer...")
        self.myText = self.txtArea.toPlainText()
        self.txtArea.textChanged.connect(self.setText)
        self.grid.addWidget(self.txtArea, 1, 1, 1, 3)

    def setText(self):
        self.myText = self.txtArea.toPlainText()

    def autoFormatWidget(self):
        self.grid.addWidget(QLabel("Shortcut Key :"), 3, 0)
        self.startKey = QComboBox()
        for i in range(1, 13):
            self.startKey.addItem("f" + str(i))

        layout = QHBoxLayout()
        self.startKey.currentIndexChanged.connect(self.setKeyText)
        layout.addWidget(QLabel("Start Key : ctrl + shift + "))
        layout.addWidget(self.startKey)
        layout.setAlignment(Qt.AlignLeft)
        delaySel = QWidget()
        delaySel.setLayout(layout)
        self.grid.addWidget(delaySel, 3, 1)

        self.stopKey = QComboBox()
        for i in range(1, 13):
            self.stopKey.addItem("f" + str(i))

        layout = QHBoxLayout()
        self.stopKey.currentIndexChanged.connect(self.setKeyText)
        layout.addWidget(QLabel("Stop Key :"))
        layout.addWidget(self.stopKey)
        layout.setAlignment(Qt.AlignLeft)
        delaySel = QWidget()
        delaySel.setLayout(layout)
        self.grid.addWidget(delaySel, 3, 2)

        self.autoFormat = QCheckBox("Reformat code/\nIDE code Typer")
        self.grid.addWidget(self.autoFormat, 4, 1)

        self.indentation = QComboBox()
        for i in range(5, 55, 5):
            self.indentation.addItem(str(i))

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Indentation fixer:"))
        layout.addWidget(self.indentation)
        layout.setAlignment(Qt.AlignLeft)
        delaySel = QWidget()
        delaySel.setLayout(layout)
        self.grid.addWidget(delaySel, 4, 2)

        self.endLines = QCheckBox("Clean Line End\n for IDE")
        self.grid.addWidget(self.endLines, 5, 1)

        self.delay = QComboBox()
        for i in range(10):
            self.delay.addItem("0." + str(i))

        layout = QHBoxLayout()
        layout.addWidget(QLabel("char Delay/sec:"))
        layout.addWidget(self.delay)
        layout.setAlignment(Qt.AlignLeft)
        keySel = QWidget()
        keySel.setLayout(layout)
        self.grid.addWidget(keySel, 5, 2)

        self.clipBoard = QCheckBox("Use Clipboard")
        self.grid.addWidget(self.clipBoard, 6, 1)

        self.lineDelay = QComboBox()
        for i in range(10):
            self.lineDelay.addItem("0." + str(i))

        print(self.lineDelay.currentText())

        layout = QHBoxLayout()
        layout.addWidget(QLabel("New Line Delay/sec:"))
        layout.addWidget(self.lineDelay)
        layout.setAlignment(Qt.AlignLeft)
        delaySel = QWidget()
        delaySel.setLayout(layout)
        self.grid.addWidget(delaySel, 6, 2)

    def setKeyText(self):
        self.grid.removeWidget(self.keyLabel)
        try:
            stop_checking_hotkeys()
            keyboard.unhook_all_hotkeys()
        except:
            pass

        self.keyLabel = QLabel("Shortcut Key=>\tctrl + shift + " +
                               self.startKey.currentText() + "\tStop: " +
                               self.stopKey.currentText())
        self.grid.addWidget(self.keyLabel, 0, 1, 1, 2)
        self.keyListener()
        self.stopTyper()

    def keyListener(self):
        def startAutoTyper():
            self.autoTyper()

        key = 'ctrl+shift+' + self.startKey.currentText()
        keyboard.add_hotkey(key, startAutoTyper, args=())

        # keyboard.wait('esc')

    def stopTyper(self):
        def stopProcess():
            self.stop = True

            print("Interrupt", self.stop)

        bindings = [
            [[self.stopKey.currentText()], None, stopProcess]
        ]
        register_hotkeys(bindings)
        start_checking_hotkeys()

    def autoTyper(self):
        try:
            if self.lineDelay.currentText() == "0.0":
                lineDelay = 0.05
            else:
                lineDelay = self.lineDelay.currentText()
            delay = self.delay.currentText()
            tabCount = int(self.indentation.currentText())
            if self.autoFormat.isChecked():
                if self.clipBoard.isChecked():
                    t = pyperclip.paste()
                    time.sleep(1)
                    l = t.split("\n")
                    for i in l:
                        if self.stop:
                            self.stop = False
                            break
                        for j in range(tabCount):
                            if self.stop:
                                # self.stop = False
                                break
                            keyboard.press_and_release('shift+tab')
                        keyboard.write(i + '\n', delay=float(delay))
                        time.sleep(float(lineDelay))

                    if self.endLines.isChecked():
                        for i in range(len(l)):
                            if self.stop:
                                self.stop = False
                                break
                            keyboard.press_and_release('ctrl+shift+l')
                        keyboard.press_and_release('backspace')
                else:
                    t = self.txtArea.toPlainText()

                    time.sleep(1)
                    l = t.split("\n")
                    for i in l:
                        if self.stop:
                            self.stop = False
                            break
                        for j in range(tabCount):
                            if self.stop:
                                # self.stop = False
                                break
                            keyboard.press_and_release('shift+tab')
                        keyboard.write(i + '\n', delay=float(delay))
                        time.sleep(float(lineDelay))

                    if self.endLines.isChecked():
                        for i in range(len(l)):
                            if self.stop:
                                self.stop = False
                                break
                            keyboard.press_and_release('ctrl+shift+l')
                        keyboard.press_and_release('backspace')
            else:
                if self.lineDelay.currentText() == "0.0" or self.lineDelay.currentText() == "0.1":
                    lineDelay = 0.2
                else:
                    lineDelay = self.lineDelay.currentText()
                delay = self.delay.currentText()

                if self.clipBoard.isChecked():
                    t = pyperclip.paste()
                    l = t.split("\n")
                    for i in l:
                        if self.stop:
                            self.stop = False
                            break
                        keyboard.write(i + '\n', delay=float(delay))
                        time.sleep(float(lineDelay))

                    if self.endLines.isChecked():
                        for i in range(len(l)):
                            if self.stop:
                                self.stop = False
                                break
                            keyboard.press_and_release('ctrl+shift+l')
                        keyboard.press_and_release('backspace')

                else:
                    t = self.txtArea.toPlainText()
                    l = t.split("\n")
                    for i in l:
                        if self.stop:
                            self.stop = False
                            break
                        keyboard.write(i + '\n', delay=float(delay))
                        time.sleep(float(lineDelay))

                    if self.endLines.isChecked():
                        for i in range(len(l)):
                            if self.stop:
                                self.stop = False
                                break
                            keyboard.press_and_release('ctrl+shift+l')
                        keyboard.press_and_release('backspace')
        except Exception as e:
            pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            stop_checking_hotkeys()
            keyboard.unhook_all_hotkeys()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    ui.keyListener()
    ui.stopTyper()
    sys.exit(app.exec_())
