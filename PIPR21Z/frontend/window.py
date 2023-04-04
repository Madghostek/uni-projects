import sys

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QKeySequence, QShortcut

from .table import SolverTableModel
from mapsolver.solver import MapSolver
from . import visualise


class MainWindow(QtWidgets.QMainWindow):
    '''
    Main window class, some controls are created and the reference
    is discarded, because it's never used, for example buttons or layouts
    '''

    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        self._app = app  # needed for ctrl+v
        self.setWindowTitle("Ocean editor")

        # QMainWindow expects a cental widget, which then is customised
        centralWidget = QtWidgets.QWidget()
        centralLayout = QtWidgets.QVBoxLayout()
        centralWidget.setLayout(centralLayout)
        centralLayout.setAlignment(QtCore.Qt.AlignTop)

        # create buttons
        bImport = QtWidgets.QPushButton("Import")
        bExport = QtWidgets.QPushButton("Export")
        bSolve = QtWidgets.QPushButton("Solve")
        bSize = QtWidgets.QPushButton("Change Size")
        # this is intended, buttons look weird when they are very long
        bImport.setMaximumSize(300, 400)
        bExport.setMaximumSize(300, 400)
        bSize.setMaximumSize(300, 400)
        bSolve.setMaximumSize(300, 400)
        bSolve.clicked.connect(self.solve)  # code can't see .clicked
        bSize.clicked.connect(self.change_size)
        bImport.clicked.connect(self.import_action)
        bExport.clicked.connect(self.export_action)

        # create simplify checkbox
        self._cSimplify = QtWidgets.QCheckBox("Cut values below ship depth")

        # create input field
        inputHBox = QtWidgets.QHBoxLayout()
        self._depthEdit = QtWidgets.QLineEdit()
        self._depthEdit.setPlaceholderText("Type ship depth here")
        self._depthEdit.setMaximumSize(200, 200)
        self._depthLabel = QtWidgets.QLabel("Required depth:")
        inputHBox.addWidget(self._depthLabel)
        inputHBox.addWidget(self._depthEdit)
        inputHBox.addStretch()

        # create solver table model instance
        self._solverModel = SolverTableModel()

        # crete and configure initial table view
        # note: QTableWidget can't change it's model
        self._tableView = QtWidgets.QTableView()
        tableHbox = QtWidgets.QHBoxLayout()
        tableHbox.addWidget(self._tableView)
        tableHbox.addStretch(1)
        self._tableView.setModel(self._solverModel)
        self._tableView.resizeColumnsToContents()  # corrects the size

        # ---messing with window and table size here---
        # allow table to adjust to contents when possible
        self._tableView.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        centralLayout.addLayout(tableHbox)
        centralLayout.addWidget(bImport)
        centralLayout.addWidget(bExport)
        centralLayout.addWidget(bSize)
        centralLayout.addWidget(bSolve)
        centralLayout.addLayout(inputHBox)
        centralLayout.addWidget(self._cSimplify)
        centralLayout.addStretch(1)

        self.setCentralWidget(centralWidget)

        QShortcut(QKeySequence('Ctrl+v'),
                  self).activated.connect(self.paste)

    # Handles ctrl+v on table, however only singular values
    def paste(self):
        clipboardText = self._app.clipboard().text()
        smodel = self._tableView.selectionModel()
        indexes = smodel.selectedIndexes()
        for idx in indexes:
            self._solverModel.setData(
                idx, clipboardText, QtCore.Qt.DisplayRole)

    # ---functions for button presses---

    @ QtCore.Slot()
    def solve(self):
        print("Solving...")
        # get input field text
        # QT ensures input validity
        depth = float(self._depthEdit.text())
        if depth > 0:
            QtWidgets.QMessageBox.information(
                self, "Error", "Is your ship flying? Please type valid depth")
            return
        simplify = self._cSimplify.isChecked()
        mapSolver = MapSolver()  # Create object that does the thing
        if mapSolver.solve_map(self._solverModel.getData(), depth):
            sol = mapSolver.getSolution()
            arg = depth if simplify else None
            visualise.show_map(self._solverModel.getData(arg), sol)
        else:
            QtWidgets.QMessageBox.information(
                self, "Info", "There is no solution")

    @ QtCore.Slot()
    def change_size(self):
        '''
        Asks user for new table size
        '''
        matSize = self._solverModel.getData().shape[0]
        msgBox = QtWidgets.QInputDialog()
        goalSize, ok = msgBox.getInt(
            self, "Change size", "New size:", matSize, 1)
        if ok:
            self._solverModel.resize(goalSize)
            self._tableView.resizeColumnsToContents()
        # else:
        #    print("Not ok")

    # import and export dialogs
    # I decided to put open() here to make tests possible,
    # this isn't a huge issue
    @ QtCore.Slot()
    def import_action(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            caption="Import map", filter="*.json")[0]
        try:
            with open(filename, "r") as f:
                self._solverModel.importJSON(f)
        # no particular exception, many bad things can happen at import
        # so this just tells user what went wrong
        except Exception as e:
            QtWidgets.QMessageBox.information(self, "Import error", str(e))
            return
        self._tableView.resizeColumnsToContents()

    @ QtCore.Slot()
    def export_action(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            caption="Export map", filter="*.json")[0]
        # when user exits from dialog
        if filename == "":
            return
        try:
            with open(filename, "w") as f:
                self._solverModel.exportJSON(f)
        except Exception as e:
            QtWidgets.QMessageBox.information(self, "Export error", str(e))


# this function starts up the window
def start():
    app = QtWidgets.QApplication(sys.argv)  # or ([]) if no cmdargs
    window = MainWindow(app)
    window.show()

    sys.exit(app.exec())
