# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'food_api.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Food_api(object):
    def setupUi(self, Food_api):
        Food_api.setObjectName("Food_api")
        Food_api.resize(1633, 700)
        self.centralwidget = QtWidgets.QWidget(Food_api)
        self.centralwidget.setObjectName("centralwidget")
        self.get_recipe = QtWidgets.QPushButton(self.centralwidget)
        self.get_recipe.setGeometry(QtCore.QRect(420, 100, 81, 28))
        self.get_recipe.setObjectName("get_recipe")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(100, 60, 771, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 40, 771, 20))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QtCore.QRect(10, 140, 941, 431))
        self.textBrowser.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.textBrowser.setObjectName("textBrowser")
        self.clear_db = QtWidgets.QPushButton(self.centralwidget)
        self.clear_db.setGeometry(QtCore.QRect(1150, 0, 131, 28))
        self.clear_db.setObjectName("clear_db")
        self.local_recipes = QtWidgets.QComboBox(self.centralwidget)
        self.local_recipes.setGeometry(QtCore.QRect(100, 100, 311, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.local_recipes.sizePolicy().hasHeightForWidth())
        self.local_recipes.setSizePolicy(sizePolicy)
        self.local_recipes.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.local_recipes.setObjectName("local_recipes")
        self.get_random_recipe = QtWidgets.QPushButton(self.centralwidget)
        self.get_random_recipe.setGeometry(QtCore.QRect(510, 100, 111, 28))
        self.get_random_recipe.setObjectName("get_random_recipe")
        self.delete_from_db = QtWidgets.QPushButton(self.centralwidget)
        self.delete_from_db.setGeometry(QtCore.QRect(630, 100, 161, 28))
        self.delete_from_db.setObjectName("delete_from_db")
        self.image_area = QtWidgets.QLabel(self.centralwidget)
        self.image_area.setGeometry(QtCore.QRect(970, 140, 556, 370))
        self.image_area.setObjectName("image_area")
        Food_api.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Food_api)
        self.statusbar.setObjectName("statusbar")
        Food_api.setStatusBar(self.statusbar)

        self.retranslateUi(Food_api)
        QtCore.QMetaObject.connectSlotsByName(Food_api)
        Food_api.setTabOrder(self.textBrowser, self.lineEdit)
        Food_api.setTabOrder(self.lineEdit, self.clear_db)
        Food_api.setTabOrder(self.clear_db, self.local_recipes)
        Food_api.setTabOrder(self.local_recipes, self.get_random_recipe)
        Food_api.setTabOrder(self.get_random_recipe, self.get_recipe)
        Food_api.setTabOrder(self.get_recipe, self.delete_from_db)

    def retranslateUi(self, Food_api):
        _translate = QtCore.QCoreApplication.translate
        Food_api.setWindowTitle(_translate("Food_api", "MainWindow"))
        self.get_recipe.setText(_translate("Food_api", "get recipe"))
        self.label.setText(_translate("Food_api", "Input ingredients:"))
        self.clear_db.setText(_translate("Food_api", "clear local database"))
        self.get_random_recipe.setText(_translate("Food_api", "get random recipe"))
        self.delete_from_db.setText(_translate("Food_api", "delete from local database"))
        self.image_area.setText(_translate("Food_api", "TextLabel"))