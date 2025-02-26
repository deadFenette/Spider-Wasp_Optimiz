import sys
import os
import csv
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QPushButton, QMessageBox, QComboBox, QGroupBox,
    QSplitter, QTableWidget, QTableWidgetItem, QStatusBar, QProgressBar,
    QFileDialog
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSettings
import importlib
from sw_optimizer.sw_optimizer import swo


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.settings = QSettings("YourCompany", "SWOOptimizer")
        self.initUI()
        self.load_theme()

    def initUI(self):
        self.setWindowTitle('SWO Optimization')
        self.setWindowIcon(QIcon('icon_spider_5.svg'))
        self.resize(1200, 800)

        self.set_base_styles()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Toolbar
        toolbar = QHBoxLayout()
        self.theme_button = QPushButton("Toggle Dark Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        toolbar.addWidget(self.theme_button)
        toolbar.addStretch()
        main_layout.addLayout(toolbar)

        # Main content splitter
        main_splitter = QSplitter(Qt.Horizontal)

        # Left Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(10)

        # Title
        title_label = QLabel('SWO Optimization Tool')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        left_layout.addWidget(title_label)

        # Function Selection
        function_group = QGroupBox('Select Test Functions')
        function_layout = QVBoxLayout()

        self.function_list = QListWidget()
        self.function_list.setSelectionMode(QListWidget.MultiSelection)
        functions = [
            "ackley", "bukin_function_n6", "eggholder_function",
            "himmelblau", "rastrigin", "rosenbrock",
            "schwefel_function", "sphere"
        ]
        for func in functions:
            self.function_list.addItem(func)

        function_layout.addWidget(self.function_list)
        function_group.setLayout(function_layout)
        left_layout.addWidget(function_group)

        # Dimension Group
        dim_group = QGroupBox('Problem Dimension')
        dim_layout = QHBoxLayout()
        self.dim_combobox = QComboBox()
        self.dim_combobox.addItems(["2", "3", "4"])
        self.dim_combobox.setToolTip("Select problem dimensionality")
        dim_layout.addWidget(self.dim_combobox)
        dim_group.setLayout(dim_layout)
        left_layout.addWidget(dim_group)

        # Run Button
        self.run_button = QPushButton('Start Optimization')
        self.run_button.setIcon(QIcon('run_icon.png'))
        self.run_button.clicked.connect(self.run_optimization)
        left_layout.addWidget(self.run_button)

        left_panel.setLayout(left_layout)
        main_splitter.addWidget(left_panel)

        # Right Panel
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)

        # Plot Widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'Fitness Value')
        self.plot_widget.setLabel('bottom', 'Iteration')
        self.plot_widget.addLegend()
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        right_layout.addWidget(self.plot_widget, 60)

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(['Function', 'Optimal Value', 'Optimal Solution'])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        right_layout.addWidget(self.results_table, 40)

        # Export Button
        export_button = QPushButton("Export Results to CSV")
        export_button.clicked.connect(self.export_results)
        right_layout.addWidget(export_button)

        right_panel.setLayout(right_layout)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([300, 800])

        main_layout.addWidget(main_splitter)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        main_layout.addWidget(self.status_bar)

        self.setLayout(main_layout)

    def set_base_styles(self):
        base_styles = """
            QWidget {
                font-family: 'Segoe UI';
                font-size: 11px;
            }
            QGroupBox {
                border: 1px solid {group_border};
                border-radius: 4px;
                margin-top: 1ex;
                color: {text_primary}; 
            }
            QPushButton {
                min-height: 28px;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QTableWidget {
                border: 1px solid {table_border};
                alternate-background-color: {table_alternate};
            }
            QHeaderView::section {
                background-color: {header_background};
                padding: 4px;
                color: {text_primary};
            }
        """
        self.light_theme = {
            'background': '#ffffff',
            'text_primary': '#2c3e50',
            'group_border': '#cccccc',
            'table_border': '#cccccc',
            'table_alternate': '#f8f8f8',
            'header_background': '#f0f0f0',
            'button_primary': '#27ae60',
            'button_hover': '#219a52'
        }

        self.dark_theme = {
            'background': '#2d2d2d',
            'text_primary': '#ffffff',
            'group_border': '#404040',
            'table_border': '#404040',
            'table_alternate': '#3a3a3a',
            'header_background': '#404040',
            'button_primary': '#27ae60',
            'button_hover': '#219a52'
        }

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.settings.setValue("dark_mode", self.dark_mode)

    def load_theme(self):
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)
        self.apply_theme()

    def apply_theme(self):
        theme = self.dark_theme if self.dark_mode else self.light_theme

        # Apply styles
        self.setStyleSheet(self.get_stylesheet(theme))

        # Update plot colors
        self.plot_widget.setBackground(theme['background'])
        self.plot_widget.getAxis('left').setPen(theme['text_primary'])
        self.plot_widget.getAxis('bottom').setPen(theme['text_primary'])
        self.plot_widget.getAxis('left').setTextPen(theme['text_primary'])
        self.plot_widget.getAxis('bottom').setTextPen(theme['text_primary'])

        # Update button text
        self.theme_button.setText("Dark Mode" if not self.dark_mode else "Light Mode")

    def get_stylesheet(self, theme):
        return f"""
            QWidget {{
                background-color: {theme['background']};
                color: {theme['text_primary']};
            }}
            QGroupBox {{
                border: 1px solid {theme['group_border']};
                color: {theme['text_primary']};
            }}
            QPushButton {{
                background-color: {theme['button_primary']};
                color: white;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
            QTableWidget {{
                border: 1px solid {theme['table_border']};
                alternate-background-color: {theme['table_alternate']};
            }}
            QHeaderView::section {{
                background-color: {theme['header_background']};
                color: {theme['text_primary']};
            }}
        """

    def run_optimization(self):
        selected_functions = [item.text() for item in self.function_list.selectedItems()]
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
        self.results_table.setRowCount(0)
        self.progress_bar.setValue(0)

        colors = ['b', 'g', 'r', 'c', 'm', 'y', (255, 165, 0), (128, 0, 128)]

        total_functions = len(selected_functions)
        for i, func_name in enumerate(selected_functions):
            func_module = importlib.import_module(func_name.lower())
            func = getattr(func_module, func_name)

            optimal_value, optimal_solution, convergence_curve, _, _ = swo(
                search_agents_no, Tmax, ub, lb, dim, func
            )

            self.status_bar.showMessage(f"Optimizing {func_name}... Done!", 5000)
            self.plot_widget.plot(convergence_curve, pen=pg.mkPen(color=colors[i % len(colors)]), name=func_name)

            row_position = self.results_table.rowCount()
            self.results_table.insertRow(row_position)
            self.results_table.setItem(row_position, 0, QTableWidgetItem(func_name))
            self.results_table.setItem(row_position, 1, QTableWidgetItem(str(optimal_value)))
            self.results_table.setItem(row_position, 2, QTableWidgetItem(str(optimal_solution)))

            # Update progress bar
            self.progress_bar.setValue(int((i + 1) / total_functions * 100))

    def export_results(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Results", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Function', 'Optimal Value', 'Optimal Solution'])
                for row in range(self.results_table.rowCount()):
                    function = self.results_table.item(row, 0).text()
                    value = self.results_table.item(row, 1).text()
                    solution = self.results_table.item(row, 2).text()
                    writer.writerow([function, value, solution])
            QMessageBox.information(self, "Export", "Results exported successfully!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())