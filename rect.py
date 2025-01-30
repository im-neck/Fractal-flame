from point import Point


class Rect:
    """
    Класс для представления прямоугольника в двумерном пространстве.

    Атрибуты:
        x (float): Координата X левого нижнего угла прямоугольника.
        y (float): Координата Y левого нижнего угла прямоугольника.
        width (float): Ширина прямоугольника.
        height (float): Высота прямоугольника.
    """

    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point: Point) -> bool:
        """
        Проверяет, находится ли точка внутри прямоугольника.

        :param point: Точка, которую нужно проверить.
        :return: True, если точка находится внутри прямоугольника, иначе False.
        """
        return self.x <= point.x <= self.x + self.width and self.y <= point.y <= self.y + self.height
