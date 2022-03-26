import sys
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QLinearGradient, QPainter, QColor, QBrush, QPaintEvent
from PySide6.QtCore import QRect, QTimer


class ProgressBarIndeterminate(QWidget):
    def __init__(self, parent=None):
        super(ProgressBarIndeterminate, self).__init__(parent)
        self.state = False
        self._value = 0
        self._direction = 1
        self._highlightWidth = 0.02
        self.colors = ["#245726", "#3fb045", "#60eb68"]
        self.setMinimumWidth(200)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateValue)
        self.setMargin(0)

    # sets colors in the order: background, secondaryHighlight, primaryHighlight
    def setColors(self, colors: list) -> None:
        assert len(colors) == 3, "Colors must be a list of 3 colors"
        self.colors = colors

    def setMargin(self, margin) -> None:
        if isinstance(margin, int):
            margin = [margin] * 4
        assert len(margin) == 4, "Margin must be a list of 4 ints"
        self.marginLeft = margin[0]
        self.marginRight = margin[2]
        self.marginTop = margin[1]
        self.marginBottom = margin[3]
        self.setBounce(False)

    def setState(self, running: bool) -> None:
        self.state = running
        self.setVisible(self.state)
        if self.state:
            self.updateValue()
        else:
            self.timer.stop()
            self.update()
        self.setVisible(self.state)

    # sets bounce property if true, the progress bar will bounce back and forth
    # it is false by default
    def setBounce(self, bounce: bool) -> None:
        if bounce:
            self.bounce = -1
        else:
            self.bounce = 1

    def updateValue(self) -> None:
        self._value = round(self._value + self._highlightWidth * self._direction, 2) % (
            1 + self._highlightWidth
        )
        if self._value == 0 or self._value == 1:
            self._direction *= self.bounce
        self.timer.start(50)
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        gradient = QLinearGradient(
            self.marginLeft,
            self.marginTop,
            painter.device().width() - self.marginRight,
            self.marginBottom,
        )
        _left = round(self._value - self._highlightWidth, 2) % (
            1 + self._highlightWidth
        )
        _right = round(self._value + self._highlightWidth, 2) % (
            1 + self._highlightWidth
        )

        gradient.setColorAt(0, QColor(self.colors[0]))
        if self._value != 1:
            gradient.setColorAt(_right, QColor(self.colors[1]))
        gradient.setColorAt(self._value, QColor(self.colors[2]))
        if self._value != 0:
            gradient.setColorAt(_left, QColor(self.colors[1]))
        gradient.setColorAt(1, QColor(self.colors[0]))
        brush = QBrush(gradient)
        rect = QRect(
            self.marginLeft,
            self.marginTop,
            painter.device().width() - self.marginRight,
            painter.device().height() - self.marginBottom,
        )
        painter.fillRect(rect, brush)
        painter.end()
