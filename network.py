import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from scapy.all import sniff, Ether

class NetworkTrafficViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Network Traffic Viewer")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Network Traffic Will Appear Here", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_traffic)
        self.timer.start(1000)  # Update every 1 second

    def update_traffic(self):
        packets = sniff(count=10, filter="icmp or tcp or udp")
        packet_info = "\n".join([str(pkt.summary()) for pkt in packets])
        self.label.setText(packet_info)

def main():
    app = QApplication(sys.argv)
    window = NetworkTrafficViewer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
