from PIL import Image
import threading
from pixel import Pixel


class FractalImage:
    """
    Класс для создания и работы с изображением фрактала.

    Атрибуты:
        width (int): Ширина изображения.
        height (int): Высота изображения.
        data (list): Двумерный список пикселей (Pixel), представляющих изображение.
        lock (threading.Lock): Объект блокировки для безопасного доступа из нескольких потоков.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data = [[Pixel() for _ in range(width)] for _ in range(height)]
        self.lock = threading.Lock()

    def contains(self, x: int, y: int) -> bool:
        """
        Проверяет, лежат ли координаты (x, y) внутри изображения.

        :param x: Координата X.
        :param y: Координата Y.
        :return: True, если координаты находятся внутри изображения, иначе False.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def add_hit(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        """
        Добавляет цвет в пиксель на позиции (x, y), с применением блокировки для многопоточности.

        :param x: Координата X.
        :param y: Координата Y.
        :param color: Кортеж из 3 целых значений (R, G, B) для цвета.
        """
        with self.lock:
            if self.contains(x, y):
                self.data[y][x].mix_color(color)

    def to_image(self) -> Image:
        """
        Преобразует данные изображения в объект PIL.Image для сохранения или отображения.

        :return: Объект изображения PIL.
        """
        img = Image.new("RGB", (self.width, self.height))
        pixels = img.load()
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.data[y][x]
                pixels[x, y] = (pixel.r, pixel.g, pixel.b)
        return img
