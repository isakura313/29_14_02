import sys
#импортируем наш sys
import json

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt #берем ядро для работы с файлами


qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file) #загружаем нашу верстку
tick = QtGui.QImage("tick.png") #получаем нашу иконку выполненного дела



class TodoModel(QtCore.QAbstractListModel):
    """
    QAbstactModel дает нам стнадратный интерфейс для модели, которая представляет наши данные
    в виде иерархического списка айтемов. Т.к. абстрактный класс, то обычно используется
    не напрямую, а используется как суперкласс
    TodoModel - в нашем случае этоsubclass
     Наша todo одна отдельная представлена в следующем виде - (False, "помыть кота")
     :status - boolean
     :text - string
    """
    def __init__(self, *args, todos = None,  **kwargs ):
        """ Наш конструктор, у которого по умолчанию нет никаких дел"""
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            """ Роль у нас на отображение, тогда нам нужно передать text"""
            _, text = self.todos[index.row()]
            #возвращаем только что полученный текст
            return text
        if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                #если status у нас имеет значение True
                return tick
                #tick у нас это галочка, думаю вы помните
    def rowCount(self, index):
        """ Метод у нас возвращает количество дел, который у нас есть"""
        return len(self.todos)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
     У нас здесь проихсходит множественное наследование от сразу двух классов
    Мы наследуем от класса главного окна
    и от класса, который имеет нашу верстку
    """
    def __init__(self):
        """метод конструктора магический у нас перед
        созданием экземпляра вызывается в последнюю очереь
        после всех остальных методов
        """
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self) #передаем экземпляру класса MainWindow нашу верстку через метод setupUi
        self.model = TodoModel() # создаем экземпляр наших дел
        self.load() #загружаем наши дела, которые были сохранены раньше в файле data.db
        self.todoView.setModel(self.model)  #todoView - это наш виджет, куда складываются все наши todo
        self.addButton.pressed.connect(self.add) #связываем с добавлением
        self.deleteButton.pressed.connect(self.delete) #связывает с удалением
        self.completeButton.pressed.connect(self.complete) # связывает с помечание дела как "Сделанного"




    def add(self):
        """
        Добавляем наш Item в QlineEdit
        потом мы очищаем нашу строку ввода после его появления в UI
        :return:
        """
        text = self.todoEdit.text() #получаем текст из нашего ввода
        if text: # не добавляет пустые строки
            self.model.todos.append((False, text))
            #запускаем перирисовку
            self.model.layoutChanged.emit()
            #очищаем наш input
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        """Функция удаления дел"""
        indexes = self.todoView.selectedIndexes() #получение индекса нашего дела
        if indexes:
            index = indexes[0]
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            #удаляем наше дело
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        """ Метод, который показывает нам, что дело сделано"""
        indexes = self.todoView.selectedIndexes()  # получение индекса нашего дела
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row]= (True, text)
            self.model.dataChanged.emit(index, index)
            self.todoView.clearSelection()
            self.save()


    def load(self):
        try:
            with open("data.db", "r") as f:
                #работаем с форматом json
                self.model.todos = json.load(f)
        except Exception:
            pass
            #но вообще здесь может быть сообщение, какая обработка
            #на например FileNotFound

    def save(self):
        #сохраняем наше дело в виде json
        with open('data.db', 'w') as f:
            data = json.dump(self.model.todos, f)


app = QtWidgets.QApplication(sys.argv)
#создаем экземпляр нашего приложения
window = MainWindow()
window.show()
app.exec_()





























