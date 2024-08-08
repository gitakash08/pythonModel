# This file contains the code for making UI with the help of pyqt python libearary 

import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox

class PredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Transporter Performance Prediction')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        formLayout = QFormLayout()
        self.truck_count = QLineEdit()
        self.invoice_count = QLineEdit()
        self.route_violation_count = QLineEdit()
        self.speed_violation_count = QLineEdit()
        self.stoppage_violation_count = QLineEdit()
        self.night_violation_count = QLineEdit()

        formLayout.addRow(QLabel('Truck Count:'), self.truck_count)
        formLayout.addRow(QLabel('Invoice Count:'), self.invoice_count)
        formLayout.addRow(QLabel('Route Violation Count:'), self.route_violation_count)
        formLayout.addRow(QLabel('Speed Violation Count:'), self.speed_violation_count)
        formLayout.addRow(QLabel('Stoppage Violation Count:'), self.stoppage_violation_count)
        formLayout.addRow(QLabel('Night Violation Count:'), self.night_violation_count)

        self.predict_button = QPushButton('Predict')
        self.predict_button.clicked.connect(self.make_prediction)

        layout.addLayout(formLayout)
        layout.addWidget(self.predict_button)

        self.setLayout(layout)

    def make_prediction(self):
        # Collect data from input fields
        data = {
            'features': [
                int(self.truck_count.text()),
                int(self.invoice_count.text()),
                int(self.route_violation_count.text()),
                int(self.speed_violation_count.text()),
                int(self.stoppage_violation_count.text()),
                int(self.night_violation_count.text())
            ]
        }
        
        try:
            response = requests.post('http://127.0.0.1:5000/predict', json=data)
            result = response.json()
            prediction = result['prediction']
            self.show_message(f'Prediction: {"In Top 10 Transporter" if prediction == 1 else "Not in Top 10"}')
        except Exception as e:
            self.show_message(f'Error: {str(e)}')

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PredictionApp()
    window.show()
    sys.exit(app.exec_())
