
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pihud.util import scale, map_scale, map_value, scale_offsets, str_scale


class Gauge2(QWidget):
    def __init__(self, parent, config):
        super(Gauge2, self).__init__(parent)

        self.config = config
        self.value = config["min"]

        self.font      = QFont()
        self.note_font = QFont()
        self.color     = QColor(config["color"])
        self.red_color = QColor(config["redline_color"])
        self.brush     = QBrush(self.color)
        self.pen       = QPen(self.color)
        self.red_pen   = QPen(self.red_color)

        self.font.setPixelSize(self.config["font_size"])
        self.note_font.setPixelSize(self.config["note_font_size"])
        self.pen.setWidth(4)
        self.red_pen.setWidth(4)

        s = scale(config["min"], config["max"], config["scale_step"])
        ss = scale(config["min"] + config["scale_step"], config["max"] - config["scale_step"], config["scale_step"])

        self.angles = map_scale(s, 0, 180)
        self.str_scale, self.multiplier = str_scale(s, config["scale_mult"])
        self.sub_angles = map_scale(ss, 22.5, 157.5)

        self.red_angle = 180
        if config["redline"] is not None:
            self.red_angle  = map_value(config["redline"], config["min"], config["max"], 0, 180)


    def render(self, response):
        # approach the value
        self.value += (response.value.magnitude - self.value) / 8
        self.update()


    def sizeHint(self):
        return QSize(350, 300)


    def paintEvent(self, e):

        r = min(self.width() / 2, self.height() / 2) #remember: radius is half of the config width
        self.__text_r     = (r / 4) * 3   # radius of the text, inside the gauge arc
        self.__tick_r     = r - 5         # outer radius of the tick marks and arc, 5 px offset from edges
        self.__tick_l     = (r / 10)      # length of each tick, extending inwards
        self.__sub_tick_l = (r / 15)      # sub tick length, extending inwards
        self.__needle_r   = (r / 20) * 17 # outer radius of the needle
        self.__needle_l   = (r / 5) * 3   # length of the needle, extending inwards

        painter = QPainter()
        painter.begin(self)

        painter.setFont(self.font)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_title(painter)
        if self.config["numerals"]:
            self.draw_multiplier(painter)
            self.draw_numbers(painter)
        self.draw_marks(painter)
        self.draw_needle(painter)

        painter.end()


    def draw_marks(self, painter):

        painter.save()

        painter.translate(self.width() / 2, self.height() / 2)


        # draw the ticks

        end = self.__tick_r - self.__tick_l

        for a in self.angles:
            painter.save()
            painter.rotate(90 + 90 + a)

            if a > self.red_angle:
                painter.setPen(self.red_pen)

            painter.drawLine(self.__tick_r - 15, 0, end, 0)  #10 px gap between arc and end of tick
            painter.restore()

        # draw the sub ticks

        end = self.__tick_r - self.__sub_tick_l

        for a in self.sub_angles:
            painter.save()
            painter.rotate(90 + 90 + a)

            if a > self.red_angle:
                painter.setPen(self.red_pen)

            painter.drawLine(self.__tick_r - 15, 0, end, 0)  #10 px gap between arc and end of tick
            painter.restore()



        # draw the arc

        p = -self.__tick_r
        d = 2 * self.__tick_r
        r = QRect(p, p, d, d)

        # arc angles are in 16th of degrees
        s = -(90 + 90) * 16
        l = -self.red_angle * 16
        painter.drawArc(r, s, l)

        painter.setPen(self.red_pen)

        s += l
        l = -(180 - self.red_angle) * 16
        painter.drawArc(r, s, l)


        painter.restore()


    def draw_numbers(self, painter):

        for a, v in zip(self.angles, self.str_scale):
            painter.save()

            if a > self.red_angle:
                painter.setPen(self.red_pen)

            painter.translate(self.width() / 2, self.height() / 2)

            painter.rotate(a)
            painter.rotate(0)                       #sets gauge start angle, 0 is straight left
            painter.translate(-self.__text_r, 0)
            painter.rotate(0)                       #sets numeral rotation, based on previous rotation
            painter.rotate(-a)

            r_width  = self.config["font_size"] * len(v)
            r_height = self.config["font_size"]

            r = QRect(-r_width / 2, -r_height / 2, r_width, r_height)
            painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, v)

            painter.restore()


    def draw_needle(self, painter):
        painter.save()

        painter.translate(self.width() / 2, self.height() / 2)
        angle = map_value(self.value, self.config["min"], self.config["max"], 0, 180)
        angle = min(angle, 180)
        angle -= 90 + 0
        painter.rotate(angle)


#        painter.drawEllipse(QPoint(0,0), 5, 5)

        painter.drawPolygon(
            QPolygon([
                QPoint(-5,  -self.__needle_l - 5),   #start point, 5 px off left flank
                QPoint(0,   -self.__needle_r),       #tip of needle
                QPoint(5,   -self.__needle_l - 5),   #5 px off right flank
                QPoint(0,   -self.__needle_l),       #tail point of needle,
                QPoint(-5,  -self.__needle_l - 5)    #return to start point
            ])
        )

        painter.restore()


    def draw_title(self, painter):
        painter.save()

        r_height = self.config["font_size"] + 20
        r = QRect(0, self.height() - r_height, self.width(), r_height)
        painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, self.config["title"])

        painter.restore()


    def draw_multiplier(self, painter):
        if self.multiplier > 1:
            painter.save()

            painter.setFont(self.note_font)
            s = "x" + str(self.multiplier)
            r = QRect(0, -self.width() / 6, self.width(), self.height())
            painter.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, s)

            painter.restore()
