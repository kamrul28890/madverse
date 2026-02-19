"""
MadVerse Animated Background Widget
Renders per-genre visual effects: flicker, glitch, sparkle, hearts, footnote, void, matrix.
"""

import math
import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer, Qt, QRectF, QPointF
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush,
                          QLinearGradient, QRadialGradient, QFont)


class Particle:
    def __init__(self, x, y, vx, vy, life, color, size, shape="circle"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = size
        self.shape = shape

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vy += 0.05  # gravity

    @property
    def alpha(self):
        return int(255 * (self.life / self.max_life))


class AnimatedBackground(QWidget):
    """
    Full-size background widget that renders animated effects.
    Place this behind all other widgets using lower z-order.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        self.effect = "none"
        self.theme = None
        self.particles: list[Particle] = []
        self.tick = 0
        self.flicker_alpha = 255
        self.glitch_offset = 0
        self.glitch_active = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update)
        self._timer.start(33)  # ~30fps

    def set_effect(self, effect: str, theme):
        self.effect = effect
        self.theme = theme
        self.particles.clear()
        self.tick = 0
        self.update()

    def _update(self):
        self.tick += 1

        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

        # Spawn new particles based on effect
        w, h = self.width(), self.height()
        if w == 0 or h == 0:
            self.update()
            return

        if self.effect == "sparkle":
            if self.tick % 3 == 0:
                for _ in range(2):
                    self.particles.append(Particle(
                        x=random.uniform(0, w),
                        y=random.uniform(0, h),
                        vx=random.uniform(-0.5, 0.5),
                        vy=random.uniform(-1.5, -0.5),
                        life=random.randint(30, 80),
                        color=QColor(255, 215, 0),
                        size=random.uniform(1.5, 4),
                        shape="star",
                    ))

        elif self.effect == "hearts":
            if self.tick % 6 == 0:
                self.particles.append(Particle(
                    x=random.uniform(w * 0.1, w * 0.9),
                    y=h + 20,
                    vx=random.uniform(-0.3, 0.3),
                    vy=random.uniform(-1.5, -0.8),
                    life=random.randint(60, 120),
                    color=QColor(255, 80, 120),
                    size=random.uniform(8, 18),
                    shape="heart",
                ))

        elif self.effect == "matrix":
            if self.tick % 4 == 0:
                for _ in range(3):
                    self.particles.append(Particle(
                        x=random.uniform(0, w),
                        y=0,
                        vx=0,
                        vy=random.uniform(2, 6),
                        life=random.randint(40, 100),
                        color=QColor(0, 255, 80),
                        size=random.uniform(8, 14),
                        shape="char",
                    ))

        elif self.effect == "void":
            if self.tick % 8 == 0:
                self.particles.append(Particle(
                    x=w / 2,
                    y=h / 2,
                    vx=random.uniform(-2, 2),
                    vy=random.uniform(-2, 2),
                    life=random.randint(50, 100),
                    color=QColor(120, 80, 200),
                    size=random.uniform(1, 3),
                    shape="circle",
                ))

        # Flicker effect
        if self.effect == "flicker":
            if random.random() < 0.03:
                self.flicker_alpha = random.randint(180, 255)
            else:
                self.flicker_alpha = min(255, self.flicker_alpha + 5)

        # Glitch effect
        if self.effect == "glitch":
            if random.random() < 0.05:
                self.glitch_active = True
                self.glitch_offset = random.randint(-8, 8)
            else:
                self.glitch_active = False
                self.glitch_offset = 0

        self.update()

    def paintEvent(self, event):
        if not self.theme:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Background gradient
        gradient = QLinearGradient(0, 0, 0, h)
        gradient.setColorAt(0, QColor(self.theme.bg_gradient_start))
        gradient.setColorAt(1, QColor(self.theme.bg_gradient_end))
        painter.fillRect(0, 0, w, h, gradient)

        # Effect-specific drawing
        if self.effect == "flicker":
            self._draw_flicker(painter, w, h)
        elif self.effect == "glitch":
            self._draw_glitch(painter, w, h)
        elif self.effect == "footnote":
            self._draw_footnote(painter, w, h)

        # Draw particles
        for p in self.particles:
            alpha = p.alpha
            if alpha <= 0:
                continue
            c = QColor(p.color)
            c.setAlpha(alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(c))

            if p.shape == "circle":
                r = p.size
                painter.drawEllipse(QRectF(p.x - r, p.y - r, r * 2, r * 2))
            elif p.shape == "star":
                self._draw_star(painter, p.x, p.y, p.size, c)
            elif p.shape == "heart":
                self._draw_heart(painter, p.x, p.y, p.size, c)
            elif p.shape == "char":
                chars = "01アイウエオ☰☷∅∞"
                char = chars[int(p.life) % len(chars)]
                painter.setPen(QPen(c))
                f = QFont("Courier New", int(p.size))
                painter.setFont(f)
                painter.drawText(int(p.x), int(p.y), char)

        painter.end()

    def _draw_flicker(self, painter, w, h):
        # Subtle red vignette
        radial = QRadialGradient(w / 2, h / 2, max(w, h) * 0.7)
        c = QColor(180, 0, 0, 0)
        radial.setColorAt(0, c)
        c2 = QColor(180, 0, 0, 40)
        radial.setColorAt(1, c2)
        painter.fillRect(0, 0, w, h, radial)

        # Random noise lines
        if random.random() < 0.1:
            pen = QPen(QColor(200, 0, 0, 30))
            pen.setWidth(1)
            painter.setPen(pen)
            for _ in range(random.randint(1, 3)):
                y = random.randint(0, h)
                painter.drawLine(0, y, w, y)

    def _draw_glitch(self, painter, w, h):
        # Scanlines
        pen = QPen(QColor(0, 212, 255, 8))
        pen.setWidth(1)
        painter.setPen(pen)
        for y in range(0, h, 4):
            painter.drawLine(0, y, w, y)

        # Neon corner accents
        pen2 = QPen(QColor(0, 212, 255, 30))
        pen2.setWidth(2)
        painter.setPen(pen2)
        size = 40
        painter.drawLine(0, 0, size, 0)
        painter.drawLine(0, 0, 0, size)
        painter.drawLine(w, 0, w - size, 0)
        painter.drawLine(w, 0, w, size)
        painter.drawLine(0, h, size, h)
        painter.drawLine(0, h, 0, h - size)
        painter.drawLine(w, h, w - size, h)
        painter.drawLine(w, h, w, h - size)

    def _draw_footnote(self, painter, w, h):
        # Lined paper effect (very subtle)
        pen = QPen(QColor(180, 170, 150, 12))
        pen.setWidth(1)
        painter.setPen(pen)
        for y in range(40, h, 28):
            painter.drawLine(20, y, w - 20, y)

        # Red margin line
        pen2 = QPen(QColor(180, 50, 50, 20))
        pen2.setWidth(1)
        painter.setPen(pen2)
        painter.drawLine(60, 0, 60, h)

    def _draw_star(self, painter, cx, cy, r, color):
        import math
        points = []
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            points.append(QPointF(cx + r * math.cos(angle), cy + r * math.sin(angle)))
            angle2 = math.radians(i * 72 - 90 + 36)
            ir = r * 0.4
            points.append(QPointF(cx + ir * math.cos(angle2), cy + ir * math.sin(angle2)))
        from PyQt6.QtGui import QPolygonF
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawPolygon(QPolygonF(points))

    def _draw_heart(self, painter, cx, cy, r, color):
        from PyQt6.QtGui import QPainterPath
        path = QPainterPath()
        s = r * 0.1
        path.moveTo(cx, cy + r * 0.3)
        path.cubicTo(cx - r * 1.1, cy - r * 0.3,
                     cx - r * 1.1, cy - r,
                     cx, cy - r * 0.4)
        path.cubicTo(cx + r * 1.1, cy - r,
                     cx + r * 1.1, cy - r * 0.3,
                     cx, cy + r * 0.3)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawPath(path)
