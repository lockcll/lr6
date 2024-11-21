from PySide6 import QtGui, QtCore, QtSql, QtWidgets
import linecache
import sys


def gomenu():
    menu = Main()
    switch.addWidget(menu)
    switch.setCurrentIndex(switch.currentIndex() + 1)


class Main(QtWidgets.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        Main.db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        host = linecache.getline('bd.txt', 1)
        host = host.strip()
        name = linecache.getline('bd.txt', 2)
        name = name.strip()
        user = linecache.getline('bd.txt', 3)
        user = user.strip()
        passw = linecache.getline('bd.txt', 4)
        passw = passw.strip()
        Main.db.setDatabaseName(name)
        Main.db.setHostName(host)
        Main.db.setUserName(user)
        Main.db.setPassword(passw)
        if not Main.db.open():
            QtWidgets.QMessageBox.critical(
                None,
                "Не удалось подключиться к БД",
                "Возникла ошибка при подключении к БД: %s" % Main.db.lastError().databaseText(), )
            sys.exit()
        Query = QtSql.QSqlQuery()
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Вагон` (`Код вагона` int NOT NULL,`Тип` varchar(20) DEFAULT NULL,`Вес` varchar(20) DEFAULT NULL,`Грузоподъемность` varchar(20),`Владелец` varchar(100) DEFAULT NULL,PRIMARY KEY (`Код вагона`))")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Груз` (`Код груза` int NOT NULL,`Вид` varchar(20) DEFAULT NULL,`Наименование` varchar(100) NOT NULL,`Вес` varchar(20) NOT NULL,PRIMARY KEY (`Код груза`))")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Заказчик` (`Код заказчика` int NOT NULL,`Наименование` varchar(100) NOT NULL,`Контактные данные` varchar(100) DEFAULT NULL,PRIMARY KEY (`Код заказчика`))")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Маршрут` (`Номер маршрута` int NOT NULL,`Станция отправления` varchar(30) NOT NULL,`Станция прибытия` varchar(30) NOT NULL,PRIMARY KEY (`Номер маршрута`))")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Отправитель` (`Код отправителя` int NOT NULL,`Наименование` varchar(100) NOT NULL,`Контактные данные` varchar(100) DEFAULT NULL,PRIMARY KEY (`Код отправителя`))")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Услуга` (`Номер услуги` int NOT NULL,`Наименование` varchar(50) NOT NULL,`Стоимость` varchar(20) NOT NULL,PRIMARY KEY (`Номер услуги`))")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Запись` (`Номер записи` int NOT NULL,`Дата` date NOT NULL,`Дата прибытия` date NOT NULL,`Дата отправки` date NOT NULL,`Код заказчика` int NOT NULL,`Получатель` varchar(100),`Код отправителя` int NOT NULL,`Плательщик` varchar(100) ,`Статус перевозки` varchar(20) NOT NULL,`Затраты на перевозку` varchar(20) DEFAULT NULL,`Стоимость перевозки` varchar(20) DEFAULT NULL,`Номер маршрута` int NOT NULL,`Номер вагона` int NOT NULL, PRIMARY KEY (`Номер записи`),KEY `Код заказчика_idx` (`Код заказчика`),KEY `Код отправителя_idx` (`Код отправителя`),KEY `Номер маршрута_idx` (`Номер маршрута`), KEY `Номер вагона_idx` (`Номер вагона`),CONSTRAINT `Код заказчика` FOREIGN KEY (`Код заказчика`) REFERENCES `заказчик` (`Код заказчика`) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT `Номер вагона` FOREIGN KEY (`Номер вагона`) REFERENCES `вагон` (`Код вагона`) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT `Код отправителя` FOREIGN KEY (`Код отправителя`) REFERENCES `отправитель` (`Код отправителя`) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT `Номер маршрута` FOREIGN KEY (`Номер маршрута`) REFERENCES `маршрут` (`Номер маршрута`) ON DELETE CASCADE ON UPDATE CASCADE)")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Перевозить груз` (`Номер погрузки` int NOT NULL,`Код груза` int NOT NULL,`Номер записи` int NOT NULL,PRIMARY KEY (`Номер погрузки`),KEY `Код груза_idx` (`Код груза`),KEY `Номер записи_idx` (`Номер записи`),CONSTRAINT `Код груза для перевозки` FOREIGN KEY (`Код груза`) REFERENCES `груз` (`Код груза`) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT `Номер записи для перевозки` FOREIGN KEY (`Номер записи`) REFERENCES `запись` (`Номер записи`) ON DELETE CASCADE ON UPDATE CASCADE)")
        Query.exec(
            "CREATE TABLE IF NOT EXISTS `Использованная услуга` (`Номер заказа` int NOT NULL,`Код услуги` int NOT NULL,`Номер записи` int NOT NULL,PRIMARY KEY (`Номер заказа`),KEY `Код использованной услуги_idx` (`Код услуги`),KEY `Код зап_idx` (`Номер записи`),CONSTRAINT `Код записи для услуги` FOREIGN KEY (`Номер записи`) REFERENCES `запись` (`Номер записи`) ON DELETE CASCADE ON UPDATE CASCADE,CONSTRAINT `Код использованной услуги` FOREIGN KEY (`Код услуги`) REFERENCES `услуга` (`Номер услуги`) ON DELETE CASCADE ON UPDATE CASCADE)")
        self.setWindowTitle('Система по учёту перевозки грузов поездами')
        pere = QtWidgets.QPushButton('Перевозка', self)
        zaka = QtWidgets.QPushButton('Заказчик', self)
        gruz = QtWidgets.QPushButton('Груз', self)
        vagon = QtWidgets.QPushButton('Вагон', self)
        mar = QtWidgets.QPushButton('Маршрут', self)
        usluga = QtWidgets.QPushButton('Услуга', self)
        otpr = QtWidgets.QPushButton('Отправитель', self)
        raschet = QtWidgets.QPushButton('Расчёт прибыли', self)
        EXIT = QtWidgets.QPushButton('Выход', self)
        ispus = QtWidgets.QPushButton('Использование услуг', self)
        menu = QtWidgets.QGridLayout()
        menu.addWidget(pere, 0, 0)
        menu.addWidget(gruz, 3, 0)
        menu.addWidget(vagon, 2, 0)
        menu.addWidget(EXIT, 4, 2, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        menu.addWidget(zaka, 1, 0)
        menu.addWidget(mar, 2, 3)
        menu.addWidget(usluga, 0, 3)
        menu.addWidget(otpr, 1, 3)
        menu.addWidget(raschet, 0, 2)
        menu.addWidget(ispus, 3, 3)
        pere.setFixedSize(200, 100)
        pere.setFont(QtGui.QFont('Arial', 25))
        ispus.setFixedSize(200, 100)
        ispus.setFont(QtGui.QFont('Arial', 15))
        raschet.setFixedSize(250, 100)
        raschet.setFont(QtGui.QFont('Arial', 25))
        otpr.setFixedSize(200, 100)
        otpr.setFont(QtGui.QFont('Arial', 25))
        usluga.setFixedSize(200, 100)
        usluga.setFont(QtGui.QFont('Arial', 25))
        mar.setFixedSize(200, 100)
        mar.setFont(QtGui.QFont('Arial', 25))
        zaka.setFixedSize(200, 100)
        zaka.setFont(QtGui.QFont('Arial', 25))
        vagon.setFixedSize(200, 100)
        vagon.setFont(QtGui.QFont('Arial', 25))
        EXIT.setFixedSize(250, 100)
        EXIT.setFont(QtGui.QFont('Arial', 25))
        gruz.setFixedSize(200, 100)
        gruz.setFont(QtGui.QFont('Arial', 25))

        self.setStyleSheet("background-color: green")
        usluga.setStyleSheet("background-color: red; color: white")
        EXIT.setStyleSheet("background-color: red; color: white")
        pere.setStyleSheet("background-color: red; color: white")
        vagon.setStyleSheet("background-color: red; color: white")
        gruz.setStyleSheet("background-color: red; color: white")
        zaka.setStyleSheet("background-color: red; color: white")
        mar.setStyleSheet("background-color: red; color: white")
        otpr.setStyleSheet("background-color: red; color: white")
        raschet.setStyleSheet("background-color: red; color: white")
        ispus.setStyleSheet("background-color: red; color: white")
        EXIT.clicked.connect(sys.exit)
        vagon.clicked.connect(self.goperevoz)
        gruz.clicked.connect(self.gogruz)
        mar.clicked.connect(self.gomar)
        zaka.clicked.connect(self.gozaka)
        pere.clicked.connect(self.gozap)
        usluga.clicked.connect(self.gousl)
        otpr.clicked.connect(self.gootrp)
        ispus.clicked.connect(self.goisu)
        raschet.clicked.connect(self.goras)
        self.setLayout(menu)

    def goras(self):
        v = Ras()
        switch.addWidget(v)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def goisu(self):
        v = Isusl()
        switch.addWidget(v)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def goperevoz(self):
        v = Vagon()
        switch.addWidget(v)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def gogruz(self):
        g = Gruz()
        switch.addWidget(g)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def gomar(self):
        m = Mar()
        switch.addWidget(m)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def gozaka(self):
        z = Zaka()
        switch.addWidget(z)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def gozap(self):
        z = Pere()
        switch.addWidget(z)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def gousl(self):
        z = Usluga()
        switch.addWidget(z)
        switch.setCurrentIndex(switch.currentIndex() + 1)

    def gootrp(self):
        z = Otpra()
        switch.addWidget(z)
        switch.setCurrentIndex(switch.currentIndex() + 1)


class Vagon(QtWidgets.QWidget):
    def __init__(self):
        super(Vagon, self).__init__()
        Vagon.mod = QtSql.QSqlTableModel(self, Main.db)
        Vagon.mod.setTable("`вагон`")
        Vagon.mod.select()
        Vagon.view = QtWidgets.QTableView()
        Vagon.view.setModel(Vagon.mod)
        Vagon.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Vagon.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Vagon.view.setStyleSheet("background-color: white; color: black")
        Vagon.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Vagon.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()

        self.setLayout(lay)

        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Vagon.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobvag()
        d.exec()

    def izm(self):
        sel = Vagon.view.selectedIndexes()[0]
        Vagon.cur = Vagon.view.model().data(sel)
        d = Izmvag()
        d.exec()

    def udal(self):
        sel = Vagon.view.selectedIndexes()[0]
        Vagon.cur = Vagon.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()
        if potw.clickedButton() == ys:
            Query.prepare("DELETE FROM Вагон WHERE `Код вагона` = :id")
            Query.bindValue(":id", Vagon.cur)
            Query.exec()
            Vagon.mod.select()


class Isusl(QtWidgets.QWidget):
    def __init__(self):
        super(Isusl, self).__init__()
        Isusl.mod = QtSql.QSqlTableModel(self, Main.db)
        Isusl.mod.setTable("использованная услуга")
        Isusl.mod.select()
        Isusl.view = QtWidgets.QTableView()
        Isusl.view.setModel(Isusl.mod)
        Isusl.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Isusl.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Isusl.view.setStyleSheet("background-color: white; color: black")
        Isusl.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Isusl.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()

        self.setLayout(lay)

        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Isusl.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobispu()
        d.exec()

    def izm(self):
        sel = Isusl.view.selectedIndexes()[0]
        Isusl.cur = Isusl.view.model().data(sel)
        d = Izmispu()
        d.exec()

    def udal(self):
        sel = Isusl.view.selectedIndexes()[0]
        Isusl.cur = Isusl.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()
        if potw.clickedButton() == ys:
            print(1)
            Query.prepare("DELETE FROM `использованная услуга` WHERE `Номер заказа` = :id")
            Query.bindValue(":id", Isusl.cur)
            Query.exec()
            Isusl.mod.select()


class Ras(QtWidgets.QWidget):
    def __init__(self):
        super(Ras, self).__init__()

        lay = QtWidgets.QGridLayout()
        self.setLayout(lay)
        self.zap = QtWidgets.QComboBox()
        Query = QtSql.QSqlQuery()
        self.zap.setFixedSize(200, 25)
        Query.exec("SELECT `Номер записи`FROM запись")
        while Query.next():
            id = Query.value(0)
            self.zap.addItem(str(id))
        a = QtWidgets.QLabel()
        a.setFixedSize(350, 50)
        a.setFont(QtGui.QFont('Arial', 25))
        a.setText('Выберите запись')
        b = QtWidgets.QLabel()
        b.setFixedSize(350, 50)
        b.setText('Итог')
        b.setFont(QtGui.QFont('Arial', 30))
        self.c = QtWidgets.QLabel()
        self.c.setFixedSize(350, 50)
        self.c.setFont(QtGui.QFont('Arial', 30))
        lay.addWidget(a, 1, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        lay.addWidget(self.zap, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        lay.addWidget(b, 2, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        lay.addWidget(self.c, 2, 1, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        a.setFont(QtGui.QFont('Arial', 30))
        dob = QtWidgets.QPushButton('Расчитать')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        a.setStyleSheet("background-color: black; color: white")
        dob.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        self.zap.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        lay.addWidget(menu, 0, 0, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        menu.clicked.connect(gomenu)
        dob.clicked.connect(self.raschi)

    def raschi(self):
        i = self.zap.currentText()
        print(i)
        z = i
        Query = QtSql.QSqlQuery()
        Query.prepare(
            "SELECT (`Стоимость перевозки`-`Затраты на перевозку`) FROM `запись` ,`услуга`,`использованная услуга`  WHERE   `запись`.`Номер записи` = :z")
        Query.bindValue(":z", z)
        Query.exec()
        while Query.next():
            st = Query.value(0)
            z = st
            self.c.setText(str(st))
        Query = QtSql.QSqlQuery()
        Query.prepare(
            "SELECT (:z+`Стоимость`) FROM `запись` ,`услуга`,`использованная услуга`  WHERE   `использованная услуга`.`Номер записи` = :i AND `использованная услуга`.`Код услуги` = `услуга`.`Номер услуги` ")
        Query.bindValue(":z", z)
        Query.bindValue(":i", i)
        Query.exec()
        while Query.next():
            st = Query.value(0)
            self.c.setText(str(st))


class Dobispu(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('использованная услуга')
        lay = QtWidgets.QGridLayout()
        self.idisp = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер заказа')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Код услуги')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Номер записи')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idisp.setValidator(QtGui.QIntValidator())
        self.idisp.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idisp, 0, 1)
        self.usl = QtWidgets.QComboBox()
        lay.addWidget(self.usl, 1, 1)
        self.zap = QtWidgets.QComboBox()
        lay.addWidget(self.zap, 2, 1)
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        Query = QtSql.QSqlQuery()
        Query.exec("SELECT `Номер услуги` FROM услуга")
        while Query.next():
            id = Query.value(0)
            self.usl.addItem(str(id))
        Query.exec("SELECT `Номер записи` FROM запись")
        while Query.next():
            id = Query.value(0)
            self.zap.addItem(str(id))

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idisp.text():
            mes.setText('Введите номер заказа')
            mes.exec()
        elif not self.usl.currentText():
            mes.setText('Выберите код услуги или добавте информацию о услугах')
            mes.exec()
        elif not self.zap.currentText():
            mes.setText('Выберите номер записи или добавте информацию о записях')
            mes.exec()
        else:
            id = self.idisp.text()
            z = self.zap.currentText()
            i = self.usl.currentText()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Номер заказа` FROM `использованная услуга` WHERE `Номер заказа` = :id")

            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            Query = QtSql.QSqlQuery()
            Query.prepare(
                "SELECT `Код услуги`,`Номер записи` FROM `использованная услуга` WHERE `Номер записи` = :z and `Код услуги` = :i")
            Query.bindValue(":z", z)
            Query.bindValue(":i", i)
            Query.exec()
            pr2 = Query.next()
            print(pr2)
            if data is False and pr2 is False:
                Query.prepare("INSERT INTO `использованная услуга` (`Номер заказа`, `Код услуги`, `Номер записи`) "
                              "VALUES (:a, :b, :c)")
                Query.bindValue(":a", self.idisp.text())
                Query.bindValue(":b", self.usl.currentText())
                Query.bindValue(":c", self.zap.currentText())
                Query.exec()
                Isusl.mod.select()
                self.close()
            else:
                mes.setText('Номер с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Izmispu(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('использованная услуга')
        lay = QtWidgets.QGridLayout()
        self.idisp = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер заказа')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Код услуги')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Номер записи')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idisp.setValidator(QtGui.QIntValidator())
        self.idisp.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idisp, 0, 1)
        self.usl = QtWidgets.QComboBox()
        lay.addWidget(self.usl, 1, 1)
        self.zap = QtWidgets.QComboBox()
        lay.addWidget(self.zap, 2, 1)
        izm = QtWidgets.QPushButton('Добавить')
        lay.addWidget(izm, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        izm.clicked.connect(self.izm)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        Query = QtSql.QSqlQuery()
        Query.exec("SELECT `Номер услуги` FROM услуга")
        while Query.next():
            id = Query.value(0)
            self.usl.addItem(str(id))
        Query.exec("SELECT `Номер записи` FROM запись")
        while Query.next():
            id = Query.value(0)
            self.zap.addItem(str(id))
        sel = Isusl.view.selectedIndexes()[0]
        self.idisp.setText(str(Isusl.view.model().data(sel)))
        sel = Isusl.view.selectedIndexes()[1]
        self.usl.setCurrentIndex(self.usl.findText(str(Isusl.view.model().data(sel))))
        sel = Isusl.view.selectedIndexes()[2]
        self.zap.setCurrentIndex(self.zap.findText(str(Isusl.view.model().data(sel))))

    def izm(self):
        mes = QtWidgets.QMessageBox()
        if not self.idisp.text():
            mes.setText('Введите номер заказа')
            mes.exec()
        elif not self.usl.currentText():
            mes.setText('Выберите код услуги или добавте информацию о услугах')
            mes.exec()
        elif not self.zap.currentText():
            mes.setText('Выберите номер записи или добавте информацию о записях')
            mes.exec()
        else:
            id = self.idisp.text()
            z = self.zap.currentText()
            i = self.usl.currentText()
            Query = QtSql.QSqlQuery()
            sel = Isusl.view.selectedIndexes()[0]
            cur = str((Isusl.view.model().data(sel)))
            Query.prepare("SELECT `Номер заказа` FROM `использованная услуга` WHERE `Номер заказа` = :id")

            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            Query = QtSql.QSqlQuery()
            Query.prepare(
                "SELECT `Код услуги`,`Номер записи` FROM `использованная услуга` WHERE `Номер записи` = :z and `Код услуги` = :i")
            Query.bindValue(":z", z)
            Query.bindValue(":i", i)
            Query.exec()
            pr2 = Query.next()
            print(pr2)
            if (data is False and pr2 is False) or (id == cur):
                Query.prepare(
                    "UPDATE `использованная услуга` SET `Номер заказа`= :a, `Код услуги`= :b, `Номер записи`= :c WHERE `Номер заказа`= :j ")

                Query.bindValue(":a", self.idisp.text())
                Query.bindValue(":b", self.usl.currentText())
                Query.bindValue(":c", self.zap.currentText())
                Query.bindValue(":j", cur)
                Query.exec()
                Isusl.mod.select()
                self.close()
            else:
                mes.setText('Номер с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Usluga(QtWidgets.QWidget):
    def __init__(self):
        super(Usluga, self).__init__()
        Usluga.mod = QtSql.QSqlTableModel(self, Main.db)
        Usluga.mod.setTable("`услуга`")
        Usluga.mod.select()
        Usluga.view = QtWidgets.QTableView()
        Usluga.view.setModel(Usluga.mod)
        Usluga.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Usluga.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Usluga.view.setStyleSheet("background-color: white; color: black")
        Usluga.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Usluga.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()
        self.setLayout(lay)
        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Usluga.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobusl()
        d.exec()

    def izm(self):
        sel = Usluga.view.selectedIndexes()[0]
        Usluga.cur = Usluga.view.model().data(sel)
        d = Izmusl()
        d.exec()

    def udal(self):
        sel = Usluga.view.selectedIndexes()[0]
        Usluga.cur = Usluga.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()

        if potw.clickedButton() == ys:
            Query.prepare("DELETE FROM Услуга WHERE `Номер услуги` = :id")
            Query.bindValue(":id", Usluga.cur)
            Query.exec()
            Usluga.mod.select()


class Dobusl(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Услуга')
        lay = QtWidgets.QGridLayout()
        self.idusl = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер услуги')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Наименование')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Стоимость')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idusl.setValidator(QtGui.QIntValidator())
        self.idusl.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idusl, 0, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(50)
        lay.addWidget(self.naimenovanie, 1, 1)
        self.stoim = QtWidgets.QLineEdit()
        self.stoim.setMaxLength(20)
        lay.addWidget(self.stoim, 2, 1)
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        self.stoim.setValidator(QtGui.QIntValidator())

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idusl.text():
            mes.setText('Введите номер услуги')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()
        elif not self.stoim.text():
            mes.setText('Введите стоимость')
            mes.exec()
        else:
            id = self.idusl.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Номер услуги` FROM Услуга WHERE `Номер услуги` = :id")
            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            if data is False:
                Query.prepare("INSERT INTO Услуга (`Номер услуги`, `Наименование`, `Стоимость`) "
                              "VALUES (:a, :b, :c)")
                Query.bindValue(":a", self.idusl.text())
                Query.bindValue(":b", self.naimenovanie.text())
                Query.bindValue(":c", self.stoim.text())
                Query.exec()
                Usluga.mod.select()
                self.close()
            else:
                mes.setText('Услуга с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Izmusl(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Услуга')
        lay = QtWidgets.QGridLayout()
        self.idusl = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер услуги')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Наименование')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Стоимость')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idusl.setValidator(QtGui.QIntValidator())
        self.idusl.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idusl, 0, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(50)
        lay.addWidget(self.naimenovanie, 1, 1)
        self.stoim = QtWidgets.QLineEdit()
        self.stoim.setMaxLength(20)
        lay.addWidget(self.stoim, 2, 1)
        izm = QtWidgets.QPushButton('Изменить')
        lay.addWidget(izm, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        izm.clicked.connect(self.izm)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        sel = Usluga.view.selectedIndexes()[0]
        self.idusl.setText(str(Usluga.view.model().data(sel)))
        sel = Usluga.view.selectedIndexes()[1]
        self.naimenovanie.setText(str(Usluga.view.model().data(sel)))
        sel = Usluga.view.selectedIndexes()[2]
        self.stoim.setText(str(Usluga.view.model().data(sel)))
        self.stoim.setValidator(QtGui.QIntValidator())

    def izm(self):
        mes = QtWidgets.QMessageBox()
        if not self.idusl.text():
            mes.setText('Введите номер услуги')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите стоимость')
            mes.exec()

        else:
            id = self.idusl.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Номер услуги` FROM Услуга WHERE `Номер услуги` = :id")
            Query.bindValue(":id", id)
            sel = Usluga.view.selectedIndexes()[0]
            cur = str((Usluga.view.model().data(sel)))
            Query.exec()
            data = Query.next()
            if (data is False) or (id == cur):
                Query.prepare(
                    "UPDATE Услуга SET `Номер услуги`= :a, `Наименование`= :b, `Стоимость`= :c WHERE `Номер услуги`= :j  ")
                Query.bindValue(":a", self.idusl.text())
                Query.bindValue(":b", self.naimenovanie.text())
                Query.bindValue(":c", self.stoim.text())
                Query.bindValue(":j", cur)
                print(Query.exec())
                Usluga.mod.select()
                self.close()
            else:
                mes.setText('Услуга с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Otpra(QtWidgets.QWidget):
    def __init__(self):
        super(Otpra, self).__init__()

        Otpra.mod = QtSql.QSqlTableModel(self, Main.db)
        Otpra.mod.setTable("`Отправитель`")
        Otpra.mod.select()
        Otpra.view = QtWidgets.QTableView()
        Otpra.view.setModel(Otpra.mod)
        Otpra.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Otpra.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Otpra.view.setStyleSheet("background-color: white; color: black")
        Otpra.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Otpra.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()
        self.setLayout(lay)
        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Otpra.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobotpr()
        d.exec()

    def izm(self):
        sel = Otpra.view.selectedIndexes()[0]
        Otpra.cur = Otpra.view.model().data(sel)
        d = Izmotpr()
        d.exec()

    def udal(self):
        sel = Otpra.view.selectedIndexes()[0]
        Otpra.cur = Otpra.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()
        if potw.clickedButton() == ys:
            Query.prepare("DELETE FROM Отправитель WHERE `Код отправителя` = :id")
            Query.bindValue(":id", Otpra.cur)
            Query.exec()
            Otpra.mod.select()


class Dobotpr(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Отправитель')
        lay = QtWidgets.QGridLayout()
        self.idotpra = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Код отправителя')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Наименование')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Контактные данные')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idotpra.setValidator(QtGui.QIntValidator())
        self.idotpra.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idotpra, 0, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(100)
        lay.addWidget(self.naimenovanie, 1, 1)
        self.contact = QtWidgets.QLineEdit()
        self.contact.setMaxLength(100)
        lay.addWidget(self.contact, 2, 1)
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idotpra.text():
            mes.setText('Введите код отправителя')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()
        else:
            id = self.idotpra.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код отправителя` FROM отправитель WHERE `Код отправителя` = :id")
            Query.bindValue(":id", id)
            data = Query.next()
            if data is False:
                Query.prepare("INSERT INTO отправитель (`Код отправителя`, `Наименование`, `Контактные данные`) "
                              "VALUES (:a, :b, :c)")
                Query.bindValue(":a", self.idotpra.text())
                Query.bindValue(":b", self.naimenovanie.text())
                Query.bindValue(":c", self.contact.text())
                Query.exec()
                Otpra.mod.select()
                self.close()
            else:
                mes.setText('Отправитель с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Izmotpr(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Отправитель')
        lay = QtWidgets.QGridLayout()
        self.idotpra = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Код отправителя')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Наименование')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Контактные данные')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idotpra.setValidator(QtGui.QIntValidator())
        self.idotpra.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idotpra, 0, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(100)
        lay.addWidget(self.naimenovanie, 1, 1)
        self.contact = QtWidgets.QLineEdit()
        self.contact.setMaxLength(100)
        lay.addWidget(self.contact, 2, 1)
        izm = QtWidgets.QPushButton('Добавить')
        lay.addWidget(izm, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        izm.clicked.connect(self.izm)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        sel = Otpra.view.selectedIndexes()[0]
        self.idotpra.setText(str(Otpra.view.model().data(sel)))
        sel = Otpra.view.selectedIndexes()[1]
        self.naimenovanie.setText(str(Otpra.view.model().data(sel)))
        sel = Otpra.view.selectedIndexes()[2]
        self.contact.setText(str(Otpra.view.model().data(sel)))

    def izm(self):
        mes = QtWidgets.QMessageBox()
        if not self.idotpra.text():
            mes.setText('Введите код отправителя')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()

        else:
            id = self.idotpra.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код отправителя` FROM отправитель WHERE `Код отправителя` = :id")
            Query.bindValue(":id", id)
            sel = Otpra.view.selectedIndexes()[0]
            cur = str((Otpra.view.model().data(sel)))
            Query.exec()
            data = Query.next()
            if (data is False) or (id == cur):
                Query.prepare(
                    "UPDATE Отправитель SET `Код отправителя`= :a, `Наименование`= :b, `Контактные данные`= :c WHERE `Код отправителя`= :j  ")
                Query.bindValue(":a", self.idotpra.text())
                Query.bindValue(":b", self.naimenovanie.text())
                Query.bindValue(":c", self.contact.text())
                Query.bindValue(":j", cur)
                print(Query.exec())
                Otpra.mod.select()
                self.close()
            else:
                mes.setText('Отправитель с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Gruz(QtWidgets.QWidget):
    def __init__(self):
        super(Gruz, self).__init__()

        Gruz.mod = QtSql.QSqlTableModel(self, Main.db)
        Gruz.mod.setTable("`груз`")
        Gruz.mod.select()
        Gruz.view = QtWidgets.QTableView()
        Gruz.view.setModel(Gruz.mod)
        Gruz.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Gruz.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Gruz.view.setStyleSheet("background-color: white; color: black")
        Gruz.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Gruz.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()
        self.setLayout(lay)
        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Gruz.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobgruz()
        d.exec()

    def izm(self):
        sel = Gruz.view.selectedIndexes()[0]
        Gruz.cur = Gruz.view.model().data(sel)
        d = Izmgruz()
        d.exec()

    def udal(self):
        sel = Gruz.view.selectedIndexes()[0]
        Gruz.cur = Gruz.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()
        if potw.clickedButton() == ys:
            Query.prepare("DELETE FROM Груз WHERE `Код груза` = :id")
            Query.bindValue(":id", Gruz.cur)
            Query.exec()
            Gruz.mod.select()


class Dobgruz(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Груз')
        lay = QtWidgets.QGridLayout()
        self.idgr = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Код груза')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Вид')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Наименование')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        d = QtWidgets.QLabel()
        d.setText('Вес')
        d.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(d, 3, 0)
        self.idgr.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idgr, 0, 1)
        self.vid = QtWidgets.QComboBox()
        self.vid.addItems(
            ['Массовый', 'Наливной', 'Навалочный', 'Насыпной', 'Лесной', 'Генеральный', 'Киповый', 'Мешковой',
             'Катно-бочковые', 'Ящичные', 'Контейнерные', 'Пакетный', 'Тарно-штучный', 'Длинномерный', 'Негабаритный',
             'Тяжеловесный', 'Живой', 'Скоропортящийся', 'Особорежимный', 'Специфический', 'Антисанитарный',
             'Негабаритный', 'Опасный'])
        lay.addWidget(self.vid, 1, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(100)
        self.ves = QtWidgets.QLineEdit()
        lay.addWidget(self.naimenovanie, 2, 1)
        lay.addWidget(self.ves, 3, 1)
        self.ves.setMaxLength(20)
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idgr.text():
            mes.setText('Введите код груза')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()
        elif not self.ves.text():
            mes.setText('Введите вес')
            mes.exec()
        else:
            id = self.idgr.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код груза` FROM Груз WHERE `Код груза` = :id")
            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            if data is False:
                Query.prepare("INSERT INTO Груз (`Код груза`, `Вид`, `Наименование`, `Вес`) "
                              "VALUES (:a, :b, :c, :d)")
                Query.bindValue(":a", self.idgr.text())
                Query.bindValue(":b", self.vid.currentText())
                Query.bindValue(":c", self.naimenovanie.text())
                Query.bindValue(":d", self.ves.text())
                Query.exec()
                Gruz.mod.select()
                self.close()
            else:
                mes.setText('Груз с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Izmgruz(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Груз')
        lay = QtWidgets.QGridLayout()
        self.idgr = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Код груза')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Вид')
        sel = Gruz.view.selectedIndexes()[0]
        self.idgr.setText(str(Gruz.view.model().data(sel)))
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Наименование')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        d = QtWidgets.QLabel()
        d.setText('Вес')
        d.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(d, 3, 0)
        self.idgr.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idgr, 0, 1)
        self.vid = QtWidgets.QComboBox()
        self.vid.addItems(
            ['Массовый', 'Наливной', 'Навалочный', 'Насыпной', 'Лесной', 'Генеральный', 'Киповый', 'Мешковой',
             'Катно-бочковые', 'Ящичные', 'Контейнерные', 'Пакетный', 'Тарно-штучный', 'Длинномерный', 'Негабаритный',
             'Тяжеловесный', 'Живой', 'Скоропортящийся', 'Особорежимный', 'Специфический', 'Антисанитарный',
             'Негабаритный', 'Опасный'])
        lay.addWidget(self.vid, 1, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(100)
        self.ves = QtWidgets.QLineEdit()
        lay.addWidget(self.naimenovanie, 2, 1)
        lay.addWidget(self.ves, 3, 1)
        self.ves.setMaxLength(20)
        sel = Gruz.view.selectedIndexes()[1]
        self.vid.setCurrentIndex(self.vid.findText(str(Gruz.view.model().data(sel))))
        sel = Gruz.view.selectedIndexes()[2]
        self.naimenovanie.setText(str(Gruz.view.model().data(sel)))
        sel = Gruz.view.selectedIndexes()[3]
        self.ves.setText(str(Gruz.view.model().data(sel)))
        izm = QtWidgets.QPushButton('Изменить')
        lay.addWidget(izm, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        izm.clicked.connect(self.izm)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)

    def izm(self):
        mes = QtWidgets.QMessageBox()
        if not self.idgr.text():
            mes.setText('Введите код груза')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()
        elif not self.ves.text():
            mes.setText('Введите вес')
            mes.exec()
        else:
            id = self.idgr.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код груза` FROM Груз WHERE `Код груза` = :id")
            Query.bindValue(":id", id)
            sel = Gruz.view.selectedIndexes()[0]
            cur = str((Gruz.view.model().data(sel)))
            Query.exec()
            data = Query.next()
            if (data is False) or (id == cur):
                Query.prepare(
                    "UPDATE Груз SET `Код груза`= :a, `Вид`= :b, `Наименование`= :c, `Вес`= :d WHERE `Код груза`= :j  ")
                Query.bindValue(":a", self.idgr.text())
                Query.bindValue(":b", self.vid.currentText())
                Query.bindValue(":c", self.naimenovanie.text())
                Query.bindValue(":d", self.ves.text())
                Query.bindValue(":j", cur)
                print(Query.exec())
                Gruz.mod.select()
                self.close()
            else:
                mes.setText('Груз с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Mar(QtWidgets.QWidget):
    def __init__(self):
        super(Mar, self).__init__()
        Mar.mod = QtSql.QSqlTableModel(self, Main.db)
        Mar.mod.setTable("`маршрут`")
        Mar.mod.select()
        Mar.view = QtWidgets.QTableView()
        Mar.view.setModel(Mar.mod)
        Mar.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Mar.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Mar.view.setStyleSheet("background-color: white; color: black")
        Mar.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Mar.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()

        self.setLayout(lay)

        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Mar.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobmar()
        d.exec()

    def izm(self):
        sel = Mar.view.selectedIndexes()[0]
        Mar.cur = Mar.view.model().data(sel)
        d = Izmmar()
        d.exec()

    def udal(self):
        sel = Mar.view.selectedIndexes()[0]
        Mar.cur = Mar.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()
        if potw.clickedButton() == ys:
            Query.prepare("DELETE FROM Маршрут WHERE `Номер маршрута` = :id")
            Query.bindValue(":id", Mar.cur)
            Query.exec()
            Mar.mod.select()


class Zaka(QtWidgets.QWidget):
    def __init__(self):
        super(Zaka, self).__init__()
        Zaka.mod = QtSql.QSqlTableModel(self, Main.db)
        Zaka.mod.setTable("`заказчик`")
        Zaka.mod.select()
        Zaka.view = QtWidgets.QTableView()
        Zaka.view.setModel(Zaka.mod)
        Zaka.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Zaka.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Zaka.view.setStyleSheet("background-color: white; color: black")
        Zaka.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Zaka.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()

        self.setLayout(lay)

        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Zaka.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobzaka()
        d.exec()

    def izm(self):
        sel = Zaka.view.selectedIndexes()[0]
        Zaka.cur = Zaka.view.model().data(sel)
        d = Izmzaka()
        d.exec()

    def udal(self):
        sel = Zaka.view.selectedIndexes()[0]
        Zaka.cur = Zaka.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()
        if potw.clickedButton() == ys:
            Query.prepare("DELETE FROM Заказчик WHERE `Код заказчика` = :id")
            Query.bindValue(":id", Zaka.cur)
            Query.exec()
            Zaka.mod.select()


class Dobzaka(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Заказчик')
        lay = QtWidgets.QGridLayout()
        self.idzaka = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Код заказчика')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Наименование')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Контактные данные')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idzaka.setValidator(QtGui.QIntValidator())
        self.idzaka.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idzaka, 0, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(100)
        lay.addWidget(self.naimenovanie, 1, 1)
        self.contact = QtWidgets.QLineEdit()
        self.contact.setMaxLength(100)
        lay.addWidget(self.contact, 2, 1)
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idzaka.text():
            mes.setText('Введите код заказчика')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()
        else:
            id = self.idzaka.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код заказчика` FROM Заказчик WHERE `Код заказчика` = :id")
            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            if data is False:
                Query.prepare("INSERT INTO Заказчик (`Код заказчика`, `Наименование`, `Контактные данные`) "
                              "VALUES (:a, :b, :c)")
                Query.bindValue(":a", self.idzaka.text())
                Query.bindValue(":b", self.naimenovanie.text())
                Query.bindValue(":c", self.contact.text())
                Query.exec()
                Zaka.mod.select()
                self.close()
            else:
                mes.setText('Маршрут с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Izmzaka(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Заказчик')
        lay = QtWidgets.QGridLayout()
        self.idzaka = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Код заказчика')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Наименование')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Конатктные данные')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idzaka.setValidator(QtGui.QIntValidator())
        self.idzaka.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idzaka, 0, 1)
        self.naimenovanie = QtWidgets.QLineEdit()
        self.naimenovanie.setMaxLength(100)
        lay.addWidget(self.naimenovanie, 1, 1)
        self.contact = QtWidgets.QLineEdit()
        self.contact.setMaxLength(100)
        lay.addWidget(self.contact, 2, 1)
        izm = QtWidgets.QPushButton('Изменение')
        lay.addWidget(izm, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        izm.clicked.connect(self.izm)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        sel = Zaka.view.selectedIndexes()[0]
        self.idzaka.setText(str(Zaka.view.model().data(sel)))
        sel = Zaka.view.selectedIndexes()[1]
        self.naimenovanie.setText(str(Zaka.view.model().data(sel)))
        sel = Zaka.view.selectedIndexes()[2]
        self.contact.setText(str(Zaka.view.model().data(sel)))

    def izm(self):
        mes = QtWidgets.QMessageBox()
        if not self.idzaka.text():
            mes.setText('Введите код заказчика')
            mes.exec()
        elif not self.naimenovanie.text():
            mes.setText('Введите наименование')
            mes.exec()

        else:
            id = self.idzaka.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код заказчика` FROM Заказчик WHERE `Код заказчика` = :id")
            Query.bindValue(":id", id)
            sel = Zaka.view.selectedIndexes()[0]
            cur = str((Zaka.view.model().data(sel)))
            Query.exec()
            data = Query.next()
            if (data is False) or (id == cur):
                Query.prepare(
                    "UPDATE Заказчик SET `Код заказчика`= :a, `Наименование`= :b, `Контактные данные`= :c WHERE `Код заказчика`= :j  ")
                Query.bindValue(":a", self.idzaka.text())
                Query.bindValue(":b", self.naimenovanie.text())
                Query.bindValue(":c", self.contact.text())
                Query.bindValue(":j", cur)
                print(Query.exec())
                Zaka.mod.select()
                self.close()
            else:
                mes.setText('Заказчик с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Pere(QtWidgets.QWidget):
    def __init__(self):
        super(Pere, self).__init__()
        Pere.mod = QtSql.QSqlTableModel(self, Main.db)
        Pere.mod.setTable("Запись")
        Pere.mod.select()
        Pere.view = QtWidgets.QTableView()
        Pere.view.setModel(Pere.mod)
        Pere.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        Pere.view.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        Pere.view.setStyleSheet("background-color: white; color: black")
        Pere.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        Pere.view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        lay = QtWidgets.QGridLayout()
        self.setLayout(lay)
        dob = QtWidgets.QPushButton('Добавить')
        izm = QtWidgets.QPushButton('Изменить')
        udal = QtWidgets.QPushButton('Удалить')
        menu = QtWidgets.QPushButton('В меню')
        dob.setFixedSize(200, 50)
        dob.setFont(QtGui.QFont('Arial', 25))
        menu.setFixedSize(200, 50)
        menu.setFont(QtGui.QFont('Arial', 25))
        izm.setFixedSize(200, 50)
        izm.setFont(QtGui.QFont('Arial', 25))
        udal.setFixedSize(200, 50)
        udal.setFont(QtGui.QFont('Arial', 25))
        dob.setStyleSheet("background-color: black; color: white")
        udal.setStyleSheet("background-color: black; color: white")
        izm.setStyleSheet("background-color: black; color: white")
        menu.setStyleSheet("background-color: black; color: white")
        lay.addWidget(dob, 0, 1)
        lay.addWidget(izm, 0, 2)
        lay.addWidget(udal, 0, 3)
        lay.addWidget(menu, 0, 0)
        lay.addWidget(Pere.view, 1, 0, 1, 4)
        dob.clicked.connect(self.dob)
        izm.clicked.connect(self.izm)
        udal.clicked.connect(self.udal)
        menu.clicked.connect(gomenu)

    def dob(self):
        d = Dobper()
        d.exec()

    def izm(self):
        sel = Pere.view.selectedIndexes()[0]
        Pere.cur = Pere.view.model().data(sel)
        d = Izmper()
        d.exec()

    def udal(self):
        sel = Pere.view.selectedIndexes()[0]
        Pere.cur = Pere.view.model().data(sel)
        Query = QtSql.QSqlQuery()
        potw = QtWidgets.QMessageBox()
        potw.setWindowTitle('Удалить запись')
        potw.setText('Вы уверены, что хотите удалить выбранную запись?')
        ys = potw.addButton('Да', QtWidgets.QMessageBox.AcceptRole)
        potw.addButton('Нет', QtWidgets.QMessageBox.RejectRole)
        potw.exec()
        if potw.clickedButton() == ys:
            Query.prepare("DELETE FROM запись WHERE `Номер записи` = :id")
            Query.bindValue(":id", Pere.cur)
            Query.exec()
            Pere.mod.select()


class Izmper(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Перевозка')
        lay = QtWidgets.QGridLayout()
        self.idper = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер записи')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Дата')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Дата прибытия')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        d = QtWidgets.QLabel()
        d.setText('Дата отправки')
        d.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(d, 3, 0)
        self.idper.setValidator(QtGui.QIntValidator())
        e = QtWidgets.QLabel()
        e.setText('Код заказчика')
        e.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(e, 4, 0)
        r = QtWidgets.QLabel()
        r.setText('Получатель')
        r.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(r, 5, 0)
        t = QtWidgets.QLabel()
        t.setText('Код отправителя')
        t.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(t, 6, 0)
        y = QtWidgets.QLabel()
        y.setText('Плательщик')
        y.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(y, 7, 0)
        y = QtWidgets.QLabel()
        y.setText('Стаутус перевозки')
        y.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(y, 8, 0)
        u = QtWidgets.QLabel()
        u.setText('Затраты на перевозку')
        u.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(u, 9, 0)
        i = QtWidgets.QLabel()
        i.setText('Стоимость перевозки')
        i.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(i, 10, 0)
        o = QtWidgets.QLabel()
        o.setText('Номер маршрута')
        o.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(o, 11, 0)
        o = QtWidgets.QLabel()
        o.setText('Номер вагона')
        o.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(o, 12, 0)
        self.idper.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idper, 0, 1)
        self.tekdate = QtWidgets.QDateEdit()
        lay.addWidget(self.tekdate, 1, 1)
        self.pribdate = QtWidgets.QDateEdit()
        lay.addWidget(self.pribdate, 2, 1)
        self.otpdate = QtWidgets.QDateEdit()
        lay.addWidget(self.otpdate, 3, 1)
        self.zakaz = QtWidgets.QComboBox()
        lay.addWidget(self.zakaz, 4, 1)
        self.poluch = QtWidgets.QLineEdit()
        self.poluch.setMaxLength(100)
        lay.addWidget(self.poluch, 5, 1)
        self.otpr = QtWidgets.QComboBox()
        lay.addWidget(self.otpr, 6, 1)
        self.platel = QtWidgets.QLineEdit()
        lay.addWidget(self.platel, 7, 1)
        self.platel.setMaxLength(100)
        self.status = QtWidgets.QComboBox()
        self.status.addItems(['Предстоит', "В процессе", "Завершена", "Отменена"])
        lay.addWidget(self.status, 8, 1)
        self.zatrat = QtWidgets.QLineEdit()
        lay.addWidget(self.zatrat, 9, 1)
        self.zatrat.setMaxLength(20)
        self.prib = QtWidgets.QLineEdit()
        lay.addWidget(self.prib, 10, 1)
        self.prib.setMaxLength(20)
        self.marh = QtWidgets.QComboBox()
        lay.addWidget(self.marh, 11, 1)
        self.vag = QtWidgets.QComboBox()
        lay.addWidget(self.vag, 12, 1)
        self.zatrat.setValidator(QtGui.QIntValidator())
        self.prib.setValidator(QtGui.QIntValidator())
        Query = QtSql.QSqlQuery()
        Query.exec("SELECT `Код заказчика` FROM заказчик")
        while Query.next():
            id = Query.value(0)
            self.zakaz.addItem(str(id))
        Query.exec("SELECT `Код отправителя` FROM отправитель")
        while Query.next():
            id = Query.value(0)
            self.otpr.addItem(str(id))
        Query.exec("SELECT  `Номер маршрута` FROM маршрут")
        while Query.next():
            id = Query.value(0)
            self.marh.addItem(str(id))
        Query.exec("SELECT  `Код вагона` FROM вагон")
        while Query.next():
            id = Query.value(0)
            self.vag.addItem(str(id))
        ism = QtWidgets.QPushButton('Изменить')
        lay.addWidget(ism, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        ism.clicked.connect(self.ism)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        sel = Pere.view.selectedIndexes()[0]
        self.idper.setText(str(Pere.view.model().data(sel)))
        sel = Pere.view.selectedIndexes()[1]
        self.tekdate.setDate(Pere.view.model().data(sel))
        sel = Pere.view.selectedIndexes()[2]
        self.pribdate.setDate(Pere.view.model().data(sel))
        sel = Pere.view.selectedIndexes()[3]
        self.otpdate.setDate(Pere.view.model().data(sel))
        sel = Pere.view.selectedIndexes()[4]
        self.zakaz.setCurrentIndex(self.zakaz.findText(str(Pere.view.model().data(sel))))
        sel = Pere.view.selectedIndexes()[5]
        self.poluch.setText(str(Pere.view.model().data(sel)))
        sel = Pere.view.selectedIndexes()[6]
        self.otpr.setCurrentIndex(self.otpr.findText(str(Pere.view.model().data(sel))))
        sel = Pere.view.selectedIndexes()[7]
        self.platel.setText(str(Pere.view.model().data(sel)))
        sel = Pere.view.selectedIndexes()[8]
        self.status.setCurrentIndex(self.status.findText(str(Pere.view.model().data(sel))))
        sel = Pere.view.selectedIndexes()[9]
        self.zatrat.setText(str(Pere.view.model().data(sel)))
        sel = Pere.view.selectedIndexes()[10]
        self.prib.setText(str(Pere.view.model().data(sel)))
        sel = Pere.view.selectedIndexes()[11]
        self.marh.setCurrentIndex(self.marh.findText(str(Pere.view.model().data(sel))))
        sel = Pere.view.selectedIndexes()[12]
        self.vag.setCurrentIndex(self.vag.findText(str(Pere.view.model().data(sel))))

    def ism(self):
        mes = QtWidgets.QMessageBox()
        if not self.idper.text():
            mes.setText('Введите номер перевозки')
            mes.exec()
        elif not self.tekdate.text():
            mes.setText('Введите дату')
            mes.exec()
        elif not self.pribdate.text():
            mes.setText('Введите дату прибытия')
            mes.exec()
        elif not self.otpdate.text():
            mes.setText('Введите дату отправления')
            mes.exec()
        elif not self.zakaz.currentText():
            mes.setText('Выберите заказчика или добавте сведения о заказчике')
            mes.exec()
        elif not self.otpr.currentText():
            mes.setText('Выберите отправителя или добавте сведения о отправителе')
            mes.exec()
        elif not self.status.currentText():
            mes.setText('Выберите статус перевозки')
            mes.exec()
        elif not self.marh.currentText():
            mes.setText('Выберите маршрут или добавте сведения о маршруте')
            mes.exec()
        elif not self.vag.currentText():
            mes.setText('Выберите вагон или добавте сведения о вагоне')
            mes.exec()
        else:
            id = self.idper.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Номер записи` FROM запись WHERE `Номер записи` = :id")
            Query.bindValue(":id", id)
            Query.exec()
            sel = Pere.view.selectedIndexes()[0]
            cur = str((Pere.view.model().data(sel)))
            data = Query.next()
            if (data is False) or (id == cur):
                Query.prepare(
                    "UPDATE Запись SET `Номер записи`= :a, `Дата`= :b, `Дата прибытия`= :c, `Дата отправки`= :d, `Код заказчика`= :e, `Получатель`= :a2, `Код отправителя`= :a3, `Плательщик`= :a4, `Статус перевозки`= :a5, `Затраты на перевозку`= :a6, `Стоимость перевозки`= :a7, `Номер маршрута`= :a8, `Номер вагона`= :a9 WHERE `Номер записи`= :j")
                Query.bindValue(":a", self.idper.text())
                Query.bindValue(":b", self.tekdate.date())
                Query.bindValue(":c", self.pribdate.date())
                Query.bindValue(":d", self.otpdate.date())
                Query.bindValue(":e", self.zakaz.currentText())
                Query.bindValue(":a2", self.poluch.text())
                Query.bindValue(":a3", self.otpr.currentText())
                Query.bindValue(":a4", self.platel.text())
                Query.bindValue(":a5", self.status.currentText())
                Query.bindValue(":a6", self.zatrat.text())
                Query.bindValue(":a7", self.prib.text())
                Query.bindValue(":a8", self.marh.currentText())
                Query.bindValue(":a9", self.vag.currentText())
                Query.bindValue(":j", cur)
                Query.exec()
                Pere.mod.select()
                self.close()
            else:
                mes.setText('Запись с данным номером уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Dobper(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Перевозка')
        lay = QtWidgets.QGridLayout()
        self.idper = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер записи')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Дата')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Дата прибытия')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        d = QtWidgets.QLabel()
        d.setText('Дата отправки')
        d.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(d, 3, 0)
        self.idper.setValidator(QtGui.QIntValidator())
        e = QtWidgets.QLabel()
        e.setText('Код заказчика')
        e.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(e, 4, 0)
        r = QtWidgets.QLabel()
        r.setText('Получатель')
        r.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(r, 5, 0)
        t = QtWidgets.QLabel()
        t.setText('Код отправителя')
        t.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(t, 6, 0)
        y = QtWidgets.QLabel()
        y.setText('Плательщик')
        y.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(y, 7, 0)
        y = QtWidgets.QLabel()
        y.setText('Стаутус перевозки')
        y.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(y, 8, 0)
        u = QtWidgets.QLabel()
        u.setText('Затраты на перевозку')
        u.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(u, 9, 0)
        i = QtWidgets.QLabel()
        i.setText('Стоимость перевозки')
        i.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(i, 10, 0)
        o = QtWidgets.QLabel()
        o.setText('Номер маршрута')
        o.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(o, 11, 0)
        o = QtWidgets.QLabel()
        o.setText('Номер вагона')
        o.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(o, 12, 0)
        self.idper.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idper, 0, 1)
        self.tekdate = QtWidgets.QDateEdit()
        lay.addWidget(self.tekdate, 1, 1)
        self.pribdate = QtWidgets.QDateEdit()
        lay.addWidget(self.pribdate, 2, 1)
        self.otpdate = QtWidgets.QDateEdit()
        lay.addWidget(self.otpdate, 3, 1)
        self.zakaz = QtWidgets.QComboBox()
        lay.addWidget(self.zakaz, 4, 1)
        self.poluch = QtWidgets.QLineEdit()
        self.poluch.setMaxLength(100)
        lay.addWidget(self.poluch, 5, 1)
        self.otpr = QtWidgets.QComboBox()
        lay.addWidget(self.otpr, 6, 1)
        self.platel = QtWidgets.QLineEdit()
        lay.addWidget(self.platel, 7, 1)
        self.platel.setMaxLength(100)
        self.status = QtWidgets.QComboBox()
        self.status.addItems(['Предстоит', "В процессе", "Завершена", "Отменена"])
        lay.addWidget(self.status, 8, 1)

        self.zatrat = QtWidgets.QLineEdit()
        lay.addWidget(self.zatrat, 9, 1)
        self.zatrat.setMaxLength(20)
        self.prib = QtWidgets.QLineEdit()
        lay.addWidget(self.prib, 10, 1)
        self.prib.setMaxLength(20)
        self.marh = QtWidgets.QComboBox()
        lay.addWidget(self.marh, 11, 1)
        self.vag = QtWidgets.QComboBox()
        lay.addWidget(self.vag, 12, 1)
        Query = QtSql.QSqlQuery()
        Query.exec("SELECT `Код заказчика` FROM заказчик")
        while Query.next():
            id = Query.value(0)
            self.zakaz.addItem(str(id))
        Query.exec("SELECT `Код отправителя` FROM отправитель")
        while Query.next():
            id = Query.value(0)
            self.otpr.addItem(str(id))
        Query.exec("SELECT  `Номер маршрута` FROM маршрут")
        while Query.next():
            id = Query.value(0)
            self.marh.addItem(str(id))
        Query.exec("SELECT  `Код вагона` FROM вагон")
        while Query.next():
            id = Query.value(0)
            self.vag.addItem(str(id))
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        self.zatrat.setValidator(QtGui.QIntValidator())
        self.prib.setValidator(QtGui.QIntValidator())

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idper.text():
            mes.setText('Введите номер перевозки')
            mes.exec()
        elif not self.tekdate.text():
            mes.setText('Введите дату')
            mes.exec()
        elif not self.pribdate.text():
            mes.setText('Введите дату прибытия')
            mes.exec()
        elif not self.otpdate.text():
            mes.setText('Введите дату отправления')
            mes.exec()
        elif not self.zakaz.currentText():
            mes.setText('Выберите заказчика или добавте сведения о заказчике')
            mes.exec()
        elif not self.otpr.currentText():
            mes.setText('Выберите отправителя или добавте сведения о отправителе')
            mes.exec()
        elif not self.status.currentText():
            mes.setText('Выберите статус перевозки')
            mes.exec()
        elif not self.marh.currentText():
            mes.setText('Выберите маршрут или добавте сведения о маршруте')
            mes.exec()
        elif not self.vag.currentText():
            mes.setText('Выберите вагон или добавте сведения о вагоне')
            mes.exec()
        else:
            id = self.idper.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Номер записи` FROM запись WHERE `Номер записи` = :id")
            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            if data is False:
                Query.prepare(
                    "INSERT INTO запись (`Номер записи`, `Дата`, `Дата прибытия`, `Дата отправки`, `Код заказчика`, `Получатель`, `Код отправителя`, `Плательщик`, `Статус перевозки`, `Затраты на перевозку`, `Стоимость перевозки`, `Номер маршрута`,`Номер вагона`) "
                    "VALUES (:a, :b, :c, :d, :e, :a2, :a3, :a4, :a5,:a6, :a7, :a8,:a9)")
                Query.bindValue(":a", self.idper.text())
                Query.bindValue(":b", self.tekdate.date())
                Query.bindValue(":c", self.pribdate.date())
                Query.bindValue(":d", self.otpdate.date())
                Query.bindValue(":e", self.zakaz.currentText())
                Query.bindValue(":a2", self.poluch.text())
                Query.bindValue(":a3", self.otpr.currentText())
                Query.bindValue(":a4", self.platel.text())
                Query.bindValue(":a5", self.status.currentText())
                Query.bindValue(":a6", self.zatrat.text())
                Query.bindValue(":a7", self.prib.text())
                Query.bindValue(":a8", self.marh.currentText())
                Query.bindValue(":a9", self.vag.currentText())
                Query.exec()
                Pere.mod.select()
                self.close()
            else:
                mes.setText('Запись с данным номером уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Dobvag(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вагон')
        lay = QtWidgets.QGridLayout()
        self.idva = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Код вагона')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Тип')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Вес')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        d = QtWidgets.QLabel()
        d.setText('Грузоподъёмность')
        d.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(d, 3, 0)
        self.idva.setValidator(QtGui.QIntValidator())
        e = QtWidgets.QLabel()
        e.setText('Владелец')
        e.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(e, 4, 0)
        self.idva.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idva, 0, 1)
        self.tip = QtWidgets.QComboBox()
        self.tip.addItems(
            ['Крытый вагон', 'Полувагон', 'Вагон-цистерна', 'Думпкар', 'Хоппер', 'Платформа', 'Фитинговыая платформа',
             'Вагон бункерного типа', 'Транспортёр', 'Автомобилевоз', 'Вагон-кенгуру', 'ИзотермическиЙ', 'Вагон-ледник',
             'Рефрижераторный', 'Вагон-термос'])
        lay.addWidget(self.tip, 1, 1)
        self.ves = QtWidgets.QLineEdit()
        self.ves.setMaxLength(20)
        lay.addWidget(self.ves, 2, 1)
        self.gruzopod = QtWidgets.QLineEdit()
        self.gruzopod.setMaxLength(20)
        self.vlad = QtWidgets.QLineEdit()
        self.vlad.setMaxLength(100)
        lay.addWidget(self.vlad, 4, 1)
        lay.addWidget(self.gruzopod, 3, 1)
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idva.text():
            mes.setText('Введите код вагона')
            mes.exec()
        else:
            id = self.idva.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код вагона` FROM Вагон WHERE `Код вагона` = :id")
            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            if data is False:
                Query.prepare("INSERT INTO Вагон (`Код вагона`, `Тип`, `Вес`, `Грузоподъемность`, `Владелец`) "
                              "VALUES (:a, :b, :c, :d, :e)")
                Query.bindValue(":a", self.idva.text())
                Query.bindValue(":b", self.tip.currentText())
                Query.bindValue(":c", self.ves.text())
                Query.bindValue(":d", self.gruzopod.text())
                Query.bindValue(":e", self.vlad.text())
                Query.exec()
                Vagon.mod.select()
                self.close()
            else:
                mes.setText('Вагон с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Izmvag(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вагон')

        lay = QtWidgets.QGridLayout()
        self.idva = QtWidgets.QLineEdit()
        sel = Vagon.view.selectedIndexes()[0]
        self.idva.setText(str(Vagon.view.model().data(sel)))
        a = QtWidgets.QLabel()
        a.setText('Код вагона')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Тип')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Вес')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        d = QtWidgets.QLabel()
        d.setText('Грузоподъёмность')
        d.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(d, 3, 0)
        self.idva.setValidator(QtGui.QIntValidator())
        e = QtWidgets.QLabel()
        e.setText('Владелец')
        e.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(e, 4, 0)
        self.idva.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idva, 0, 1)
        self.tip = QtWidgets.QComboBox()

        self.tip.addItems(
            ['Крытый вагон', 'Полувагон', 'Вагон-цистерна', 'Думпкар', 'Хоппер', 'Платформа', 'Фитинговыая платформа',
             'Вагон бункерного типа', 'Транспортёр', 'Автомобилевоз', 'Вагон-кенгуру', 'ИзотермическиЙ', 'Вагон-ледник',
             'Рефрижераторный', 'Вагон-термос'])
        lay.addWidget(self.tip, 1, 1)
        self.ves = QtWidgets.QLineEdit()
        sel = Vagon.view.selectedIndexes()[1]
        self.tip.setCurrentIndex(self.tip.findText(str(Vagon.view.model().data(sel))))
        self.ves.setMaxLength(20)
        lay.addWidget(self.ves, 2, 1)
        sel = Vagon.view.selectedIndexes()[2]
        self.ves.setText(str(Vagon.view.model().data(sel)))
        self.gruzopod = QtWidgets.QLineEdit()
        self.gruzopod.setMaxLength(20)
        sel = Vagon.view.selectedIndexes()[3]
        self.gruzopod.setText(str(Vagon.view.model().data(sel)))
        self.vlad = QtWidgets.QLineEdit()
        self.vlad.setMaxLength(100)
        sel = Vagon.view.selectedIndexes()[4]
        self.vlad.setText(str(Vagon.view.model().data(sel)))
        lay.addWidget(self.vlad, 4, 1)
        lay.addWidget(self.gruzopod, 3, 1)
        izm = QtWidgets.QPushButton('Изменить')
        lay.addWidget(izm, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        izm.clicked.connect(self.izm)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)

    def izm(self):
        mes = QtWidgets.QMessageBox()
        if not self.idva.text():
            mes.setText('Введите код вагона')
            mes.exec()
        else:
            id = self.idva.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Код вагона` FROM Вагон WHERE `Код вагона` = :id")
            Query.bindValue(":id", id)
            sel = Vagon.view.selectedIndexes()[0]
            cur = str((Vagon.view.model().data(sel)))
            Query.exec()
            data = Query.next()
            if (data is False) or (id == cur):
                Query.prepare(
                    "UPDATE Вагон SET `Код вагона`= :a, `Тип`= :b, `Вес`= :c, `Грузоподъемность`= :d, `Владелец`= :e WHERE `Код вагона`= :j  ")
                Query.bindValue(":a", self.idva.text())
                Query.bindValue(":b", self.tip.currentText())
                Query.bindValue(":c", self.ves.text())
                Query.bindValue(":d", self.gruzopod.text())
                Query.bindValue(":e", self.vlad.text())
                Query.bindValue(":j", cur)
                print(Query.exec())
                Vagon.mod.select()
                self.close()
            else:
                mes.setText('Вагон с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Dobmar(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Маршрут')
        lay = QtWidgets.QGridLayout()
        self.idmar = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер маршрута')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Станция отправления')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Станция прибытия')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idmar.setValidator(QtGui.QIntValidator())
        self.idmar.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idmar, 0, 1)
        self.otpr = QtWidgets.QLineEdit()
        self.otpr.setMaxLength(30)
        lay.addWidget(self.otpr, 1, 1)
        self.prib = QtWidgets.QLineEdit()
        self.prib.setMaxLength(30)
        lay.addWidget(self.prib, 2, 1)
        dob = QtWidgets.QPushButton('Добавить')
        lay.addWidget(dob, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        dob.clicked.connect(self.dob)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)

    def dob(self):
        mes = QtWidgets.QMessageBox()
        if not self.idmar.text():
            mes.setText('Введите номер маршрута')
            mes.exec()
        elif not self.otpr.text():
            mes.setText('Введите станцию отправления')
            mes.exec()
        elif not self.prib.text():
            mes.setText('Введите станцию прибытия')
            mes.exec()
        else:
            id = self.idmar.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Номер маршрута` FROM Маршрут WHERE `Номер маршрута` = :id")
            Query.bindValue(":id", id)
            Query.exec()
            data = Query.next()
            if data is False:
                Query.prepare("INSERT INTO Маршрут (`Номер маршрута`, `Станция отправления`, `Станция прибытия`) "
                              "VALUES (:a, :b, :c)")
                Query.bindValue(":a", self.idmar.text())
                Query.bindValue(":b", self.otpr.text())
                Query.bindValue(":c", self.prib.text())
                Query.exec()
                Mar.mod.select()
                self.close()
            else:
                mes.setText('Маршрут с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


class Izmmar(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Маршрут')
        lay = QtWidgets.QGridLayout()
        self.idmar = QtWidgets.QLineEdit()
        a = QtWidgets.QLabel()
        a.setText('Номер маршрута')
        lay.addWidget(a, 0, 0)
        b = QtWidgets.QLabel()
        b.setText('Станция отправления')
        a.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(b, 1, 0)
        c = QtWidgets.QLabel()
        c.setText('Станция прибытия')
        c.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(c, 2, 0)
        self.idmar.setValidator(QtGui.QIntValidator())
        self.idmar.setValidator(QtGui.QIntValidator())
        b.setFont(QtGui.QFont('Arial', 10))
        lay.addWidget(self.idmar, 0, 1)
        self.otpr = QtWidgets.QLineEdit()
        self.otpr.setMaxLength(30)
        lay.addWidget(self.otpr, 1, 1)
        self.prib = QtWidgets.QLineEdit()
        self.prib.setMaxLength(30)
        lay.addWidget(self.prib, 2, 1)
        izm = QtWidgets.QPushButton('Изменить')
        lay.addWidget(izm, 5, 3, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        self.setLayout(lay)
        self.setMinimumSize(500, 200)
        izm.clicked.connect(self.izm)
        otm = QtWidgets.QPushButton('Отмена')
        lay.addWidget(otm, 5, 4, alignment=QtCore.Qt.AlignmentFlag.AlignBottom)
        otm.clicked.connect(self.otm)
        sel = Mar.view.selectedIndexes()[0]
        self.idmar.setText(str(Mar.view.model().data(sel)))
        sel = Mar.view.selectedIndexes()[1]
        self.otpr.setText(str(Mar.view.model().data(sel)))
        sel = Mar.view.selectedIndexes()[2]
        self.prib.setText(str(Mar.view.model().data(sel)))

    def izm(self):
        mes = QtWidgets.QMessageBox()
        if not self.idmar.text():
            mes.setText('Введите номер маршрута')
            mes.exec()
        elif not self.otpr.text():
            mes.setText('Введите станцию отправления')
            mes.exec()
        elif not self.prib.text():
            mes.setText('Введите станцию прибытия')
            mes.exec()
        else:
            id = self.idmar.text()
            Query = QtSql.QSqlQuery()
            Query.prepare("SELECT `Номер маршрута` FROM Маршрут WHERE `Номер маршрута` = :id")
            Query.bindValue(":id", id)
            sel = Mar.view.selectedIndexes()[0]
            cur = str((Mar.view.model().data(sel)))
            Query.exec()
            data = Query.next()
            if (data is False) or (id == cur):
                Query.prepare(
                    "UPDATE Маршрут SET `Номер маршрута`= :a, `Станция отправления`= :b, `Станция прибытия`= :c WHERE `Номер маршрута`= :j  ")
                Query.bindValue(":a", self.idmar.text())
                Query.bindValue(":b", self.otpr.text())
                Query.bindValue(":c", self.prib.text())
                Query.bindValue(":j", cur)
                print(Query.exec())
                Mar.mod.select()
                self.close()
            else:
                mes.setText('Маршрут с данным кодом уже существует')
                mes.exec()

    def otm(self):
        self.close()


app = QtWidgets.QApplication([])
switch = QtWidgets.QStackedWidget()
menu = Main()
switch.addWidget(menu)
switch.setStyleSheet("background-color: blue")
switch.setWindowTitle('Система по учёту перевозки грузов поездами')
switch.setMinimumSize(1000, 700)
switch.show()
app.exec()
