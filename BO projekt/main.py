from App import *

import random
import BOpack as bo
import matplotlib.pyplot as plt
import testModule

# TODO wyświetlanie komunikatow w oknie aplikacji zamiast konosli

if __name__ == '__main__':
    print('Waiting for app...')
    app = QApplication(sys.argv)
    ex = MainWindow()
    print('App runnig')
    sys.exit(app.exec_())