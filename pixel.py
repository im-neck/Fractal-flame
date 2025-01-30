class Pixel:
    """
    Класс для представления пикселя в изображении.

    Атрибуты:
        r (int): Значение компоненты красного цвета (от 0 до 255).
        g (int): Значение компоненты зелёного цвета (от 0 до 255).
        b (int): Значение компоненты синего цвета (от 0 до 255).
        hit_count (int): Счётчик количества попаданий цвета в данный пиксель.
    """

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, hit_count: int = 0):

        self.r = r
        self.g = g
        self.b = b
        self.hit_count = hit_count

    def mix_color(self, color: tuple[int, int, int], weight: int = 1) -> None:
        """
        Смешивает текущий цвет пикселя с новым цветом с учётом веса.

        :param color: Кортеж с тремя значениями (R, G, B) для нового цвета.
        :param weight: Важность нового цвета при смешивании (по умолчанию 1).
        """
        self.r = int((self.r * self.hit_count + color[0] * weight) / (self.hit_count + weight))
        self.g = int((self.g * self.hit_count + color[1] * weight) / (self.hit_count + weight))
        self.b = int((self.b * self.hit_count + color[2] * weight) / (self.hit_count + weight))
        self.hit_count += 1
