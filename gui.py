import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton, QMessageBox, QComboBox
import pyqtgraph as pg
import numpy as np
import importlib
import os
from sw_optimizer.sw_optimizer import swo

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SWO Optimization')

        layout = QVBoxLayout()

        self.function_label = QLabel('Select Functions:')
        layout.addWidget(self.function_label)

        self.function_checkboxes = []
        functions = ["ackley", "bukin_function_n6", "eggholder_function", "himmelblau", "rastrigin", "rosenbrock", "schwefel_function", "sphere"]
        for func in functions:
            checkbox = QCheckBox(func)
            self.function_checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        self.dim_label = QLabel('Dimension:')
        layout.addWidget(self.dim_label)

        self.dim_combobox = QComboBox()
        self.dim_combobox.addItems(["2", "3", "4"])
        layout.addWidget(self.dim_combobox)

        self.run_button = QPushButton('Run Optimization')
        self.run_button.clicked.connect(self.run_optimization)
        layout.addWidget(self.run_button)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.addLegend()  # Добавляем легенду
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

    def run_optimization(self):
        selected_functions = [checkbox.text() for checkbox in self.function_checkboxes if checkbox.isChecked()]
        if not selected_functions:
            QMessageBox.warning(self, "Warning", "Please select at least one function.")
            return

        dim = int(self.dim_combobox.currentText())

        search_agents_no = 30
        Tmax = 1000
        lb = [-512] * dim
        ub = [512] * dim

        test_functions_dir = os.path.join(os.path.dirname(__file__), 'test_functions')
        sys.path.append(test_functions_dir)

        self.plot_widget.clear()

        colors = [
            'b',  # синий
            'g',  # зеленый
            'r',  # красный
            'c',  # голубой
            'm',  # пурпурный
            'y',  # желтый
            (255, 165, 0),  # оранжевый
            (128, 0, 128),  # фиолетовый
            (0, 255, 255),  # бирюзовый
            (255, 20, 147),  # розовый
            (255, 255, 0),  # желтый
            (0, 255, 0),  # светло-зеленый
            (160, 32, 240),  # светло-пурпурный
            (0, 191, 255),  # светло-голубой
            (220, 20, 60)    # светло-красный
        ]

        for i, func_name in enumerate(selected_functions):
            func_module = importlib.import_module(func_name.lower())
            func = getattr(func_module, func_name)

            optimal_value, optimal_solution, convergence_curve, total_evaluations, evaluations_per_function = swo(
                search_agents_no, Tmax, ub, lb, dim, func)

            QMessageBox.information(self, "Results", f"Optimal Value: {optimal_value}\nOptimal Solution: {optimal_solution}\nTotal Evaluations: {total_evaluations}")

            self.plot_widget.plot(convergence_curve, pen=pg.mkPen(color=colors[i % len(colors)]), name=func_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
