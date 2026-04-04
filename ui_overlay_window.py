# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'overlay_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_OverlayWindow(object):
    def setupUi(self, OverlayWindow):
        if not OverlayWindow.objectName():
            OverlayWindow.setObjectName(u"OverlayWindow")
        OverlayWindow.resize(380, 100)
        OverlayWindow.setMaximumSize(QSize(380, 100))
        self.verticalLayout = QVBoxLayout(OverlayWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Status = QLabel(OverlayWindow)
        self.Status.setObjectName(u"Status")

        self.verticalLayout.addWidget(self.Status)

        self.StatusStream = QLabel(OverlayWindow)
        self.StatusStream.setObjectName(u"StatusStream")

        self.verticalLayout.addWidget(self.StatusStream)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.OverlayRun = QPushButton(OverlayWindow)
        self.OverlayRun.setObjectName(u"OverlayRun")

        self.buttonLayout.addWidget(self.OverlayRun)

        self.OverlayPause = QPushButton(OverlayWindow)
        self.OverlayPause.setObjectName(u"OverlayPause")

        self.buttonLayout.addWidget(self.OverlayPause)

        self.OverlayResume = QPushButton(OverlayWindow)
        self.OverlayResume.setObjectName(u"OverlayResume")

        self.buttonLayout.addWidget(self.OverlayResume)

        self.OverlayStop = QPushButton(OverlayWindow)
        self.OverlayStop.setObjectName(u"OverlayStop")

        self.buttonLayout.addWidget(self.OverlayStop)


        self.verticalLayout.addLayout(self.buttonLayout)


        self.retranslateUi(OverlayWindow)

        QMetaObject.connectSlotsByName(OverlayWindow)
    # setupUi

    def retranslateUi(self, OverlayWindow):
        OverlayWindow.setWindowTitle(QCoreApplication.translate("OverlayWindow", u"Overlay", None))
        self.Status.setText(QCoreApplication.translate("OverlayWindow", u"Status:", None))
        self.StatusStream.setText(QCoreApplication.translate("OverlayWindow", u"Step: Waiting", None))
        self.OverlayRun.setText(QCoreApplication.translate("OverlayWindow", u"Run", None))
        self.OverlayPause.setText(QCoreApplication.translate("OverlayWindow", u"Pause", None))
        self.OverlayResume.setText(QCoreApplication.translate("OverlayWindow", u"Resume", None))
        self.OverlayStop.setText(QCoreApplication.translate("OverlayWindow", u"Stop", None))
    # retranslateUi

