# main.py
import sys
from PyQt5.QtWidgets import QApplication
from menu_window import MenuWindow

def main():
    app = QApplication(sys.argv)
    menu = MenuWindow()
    menu.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()