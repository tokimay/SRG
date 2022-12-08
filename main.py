"""
1 - start mic stream
2 - graph(spectrum & FFT) and play
3 - save to postgresql (DB=sound, user=python, pass=python, table=storage)
4 - get from postgresql
5 - graph and play

tokimay@gmail.com
"""
import psycopg2
import pyaudio
import sys
import graph
import wave
import matplotlib.pyplot as plt
import numpy as np
import struct

from PySide6.QtWidgets import QApplication, QMainWindow
from PIL import Image
from PySide6 import QtGui
from PySide6.QtWidgets import QSizePolicy
from urllib.parse import urlparse


class MainWindow(QMainWindow):
    def __init__(self):
        self.frame = []
        self.stop = False
        self.id = 0
        super(MainWindow, self).__init__()
        self.ui = graph.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_start.clicked.connect(lambda: self.playBack_record_spectrum_stream())
        self.ui.pushButton_stop.clicked.connect(lambda: self.stop_record())
        self.ui.pushButton_play.clicked.connect(lambda: self.play_spectrum_file())
        conStr = "localhost://python:python@sound:5432"
        p = urlparse(conStr)
        pg_connection_dict = {'dbname': p.hostname, 'user': p.username,
                              'password': p.password, 'port': p.port, 'host': p.scheme}

        print(pg_connection_dict)
        con = psycopg2.connect(**pg_connection_dict)
        print(con)
        cur = con.cursor()
        cur.execute('DROP TABLE storage')
        cur.execute('CREATE TABLE storage (id   Integer, record  bytea[])')
        cur.execute('ALTER TABLE storage OWNER TO python')
        con.commit()

    @staticmethod
    def def_stream():
        CHUNK = 1024
        P = pyaudio.PyAudio()
        RATE = 44100
        FORMAT = pyaudio.paInt16
        STREAM = P.open(format=FORMAT,
                        channels=1,
                        rate=RATE,
                        output=True,
                        input=True,
                        input_device_index=0,  # my mic device index is 0
                        )
        STREAM.start_stream()
        return STREAM, P, CHUNK, RATE, FORMAT

    def playBack_record_spectrum_stream(self, file_name=None):
        STREAM, P, CHUNK, RATE, FORMAT = MainWindow.def_stream()
        self.stop = False

        fig, (ax, ax1) = plt.subplots(2)
        x_fft = np.linspace(0, RATE, CHUNK)
        line_fft, = ax1.semilogx(x_fft, np.random.rand(CHUNK), 'b')
        x = np.arange(0, 2 * CHUNK, 2)
        line, = ax.plot(x, np.random.rand(CHUNK), 'r')
        ax.set_ylim(-50000, 50000)
        ax1.set_ylim(0, 5)
        ax.ser_xlim = (0, CHUNK)
        ax1.set_xlim(20, RATE / 2)

        frames = []

        while not self.stop:
            data = STREAM.read(CHUNK, exception_on_overflow=False)
            STREAM.write(data)  # play back
            frames.append(data)

            dataInt = struct.unpack(str(CHUNK) + 'h', data)

            line.set_ydata(dataInt)
            line_fft.set_ydata(np.abs(np.fft.fft(dataInt)) * 2 / (11000 * CHUNK))

            fig.canvas.draw()

            image = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
            im2 = image.convert("RGBA")
            data = im2.tobytes("raw", "BGRA")
            qim = QtGui.QImage(data, image.width, image.height, QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap.fromImage(qim)
            self.ui.pic_label.setPixmap(pixmap)
            self.ui.pic_label.show()
            self.ui.pic_label.setScaledContents(True)
            self.ui.pic_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            fig.canvas.flush_events()
        if file_name is not None:
            f = wave.open(file_name, 'wb')
            f.setnchannels(1)
            f.setsampwidth(P.get_sample_size(FORMAT))
            f.setframerate(RATE)
            f.writeframes(b''.join(frames))
            f.close()

        conStr = "localhost://python:python@sound:5432"
        p = urlparse(conStr)
        pg_connection_dict = {'dbname': p.hostname, 'user': p.username,
                              'password': p.password, 'port': p.port, 'host': p.scheme}

        print(pg_connection_dict)
        con = psycopg2.connect(**pg_connection_dict)
        print(con)
        cur = con.cursor()
        cur.execute('INSERT INTO storage VALUES (%s, %s)', (self.id, frames))
        con.commit()
        self.id = self.id + 1
        STREAM.stop_stream()
        STREAM.close()
        P.terminate()

    def play_spectrum_file(self):
        STREAM, P, CHUNK, RATE, FORMAT = MainWindow.def_stream()
        self.stop = False
        fig, (ax, ax1) = plt.subplots(2)
        x_fft = np.linspace(0, RATE, CHUNK)
        line_fft, = ax1.semilogx(x_fft, np.random.rand(CHUNK), 'b')
        x = np.arange(0, 2 * CHUNK, 2)
        line, = ax.plot(x, np.random.rand(CHUNK), 'r')
        ax.set_ylim(-50000, 50000)
        ax1.set_ylim(0, 5)
        ax.ser_xlim = (0, CHUNK)
        ax1.set_xlim(20, RATE / 2)

        # wf = wave.open(file_name, 'rb')  # mono
        conStr = "localhost://python:python@sound:5432"
        p = urlparse(conStr)
        pg_connection_dict = {'dbname': p.hostname, 'user': p.username,
                              'password': p.password, 'port': p.port, 'host': p.scheme}

        print(pg_connection_dict)
        con = psycopg2.connect(**pg_connection_dict)
        print(con)
        cur = con.cursor()
        cur.execute("SELECT record FROM storage WHERE id=%s", (self.id-1,))
        results = cur.fetchall()
        print(results)
        con.commit()
        i = 0
        # data = wf.readframes(CHUNK)
        data = results[0][0][i].tobytes()
        while not self.stop:
            STREAM.write(data)
            dataInt = struct.unpack(str(CHUNK) + 'h', data)
            line.set_ydata(dataInt)
            line_fft.set_ydata(np.abs(np.fft.fft(dataInt)) * 2 / (11000 * CHUNK))
            fig.canvas.draw()
            image = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
            im2 = image.convert("RGBA")
            data = im2.tobytes("raw", "BGRA")
            qim = QtGui.QImage(data, image.width, image.height, QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap.fromImage(qim)
            self.ui.pic_label.setPixmap(pixmap)
            self.ui.pic_label.show()
            self.ui.pic_label.setScaledContents(True)
            self.ui.pic_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            fig.canvas.flush_events()
            # data = wf.readframes(CHUNK)
            i = i + 1
            data = results[0][0][i].tobytes()

        STREAM.stop_stream()
        STREAM.close()
        P.terminate()

    def stop_record(self):
        self.stop = True


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
