import random
from concurrent.futures import ThreadPoolExecutor
from math import sin, cos, pi, sqrt

from rect import Rect
from point import Point
from fractal_image import FractalImage


def spherical(point: Point) -> Point:
    """
    Сферическая трансформация точки.

    :param point: исходная точка
    :return: трансформированная точка
    """
    r2 = point.x ** 2 + point.y ** 2
    if r2 == 0:
        return Point(0, 0)
    return Point(point.x / r2, point.y / r2)


def sinusoidal(point: Point) -> Point:
    """
    Синусоидальная трансформация точки.

    :param point: исходная точка
    :return: трансформированная точка
    """
    return Point(sin(point.x), sin(point.y))


def diamond(point: Point) -> Point:
    """
    Алмазная трансформация точки.

    :param point: исходная точка
    :return: трансформированная точка
    """
    return Point(abs(point.x), abs(point.y))


def fish(point: Point) -> Point:
    """
    Трансформация рыбки.

    :param point: исходная точка
    :return: трансформированная точка
    """
    return Point(point.x + sin(point.y), point.y + sin(point.x))


def swirl(point: Point) -> Point:
    """
    Спиральная трансформация точки.

    :param point: исходная точка
    :return: трансформированная точка
    """
    r2 = point.x ** 2 + point.y ** 2
    return Point(
        point.x * sin(r2) - point.y * cos(r2),
        point.x * cos(r2) + point.y * sin(r2)
    )


def linear(point: Point) -> Point:
    """
    Линейная трансформация точки (без изменений).

    :param point: исходная точка
    :return: та же точка
    """
    return point


TRANSFORMATIONS = [spherical, sinusoidal, swirl, linear, diamond, fish]


def random_point_in_rect(rect: Rect) -> Point:
    """
    Генерация случайной точки в пределах прямоугольника.

    :param rect: прямоугольник, в пределах которого генерируется точка
    :return: случайная точка
    """
    return Point(
        random.uniform(rect.x, rect.x + rect.width),
        random.uniform(rect.y, rect.y + rect.height)
    )


def map_to_pixel(rect: Rect, point: Point, image: FractalImage) -> tuple[int, int] | None:
    """
    Преобразование координат точки в пиксельные координаты изображения.

    :param rect: область в мировых координатах
    :param point: точка в мировых координатах
    :param image: объект изображения, на котором рисуем
    :return: координаты пикселя или None, если точка не попадает в изображение
    """
    x = int((point.x - rect.x) / rect.width * image.width)
    y = int((point.y - rect.y) / rect.height * image.height)
    if image.contains(x, y):
        return x, y
    return None


def generate_fractal(image: FractalImage, world: Rect, transformations: list, samples: int, iter_per_sample: int,
                     symmetry: int = 1):
    """
    Генерация фрактала.

    :param image: объект изображения, на котором рисуем
    :param world: мировая область
    :param transformations: список трансформаций для фрактала
    :param samples: количество выборок
    :param iter_per_sample: количество итераций на выборку
    :param symmetry: симметрия фрактала (по умолчанию 1)
    """
    for _ in range(samples):
        point = random_point_in_rect(world)
        for _ in range(iter_per_sample):
            transform = random.choice(transformations)
            point = transform(point)

            for s in range(symmetry):
                theta = 2 * pi * s / symmetry
                rotated_point = Point(
                    point.x * cos(theta) - point.y * sin(theta),
                    point.x * sin(theta) + point.y * cos(theta)
                )

                pixel_coords = map_to_pixel(world, rotated_point, image)
                if pixel_coords:
                    color = (int(255 * random.random()), int(255 * random.random()), int(255 * random.random()))
                    image.add_hit(pixel_coords[0], pixel_coords[1], color)


def save_image(image: FractalImage, filename: str):
    """
    Сохранение изображения в файл.

    :param image: объект изображения
    :param filename: имя файла для сохранения
    """
    img = image.to_image()
    img.save(filename)


def get_valid_input(prompt: str, value_type: type = int, min_value: int | None = None,
                    max_value: int | None = None) -> int:
    """
    Безопасный ввод с проверкой значений.

    :param prompt: запрос к пользователю
    :param value_type: тип данных, который ожидается от пользователя
    :param min_value: минимальное допустимое значение
    :param max_value: максимальное допустимое значение
    :return: введённое значение
    """
    while True:
        try:
            user_input = value_type(input(prompt))

            if (min_value is not None and user_input < min_value) or (max_value is not None and user_input > max_value):
                print(f"Ошибка: введите значение в пределах {min_value} - {max_value}.")
                continue

            return user_input
        except ValueError:
            print(f"Ошибка: введите корректное значение для {prompt.strip()[:-1]}.")


def user_input() -> tuple[int, int, int, int, list, bool, int]:
    """
    Запрос настроек у пользователя для генерации фрактала.

    :return: кортеж с параметрами: ширина, высота, количество выборок, количество итераций,
             выбранные трансформации, использование многозадачности и количество потоков
    """
    print("Настройка параметров генерации фрактала:\n")

    width = get_valid_input("Введите ширину изображения (например, 800): ", value_type=int, min_value=1)
    height = get_valid_input("Введите высоту изображения (например, 600): ", value_type=int, min_value=1)

    samples = get_valid_input("Введите количество выборок (например, 100000): ", value_type=int, min_value=1)

    iter_per_sample = get_valid_input("Введите количество итераций на выборку (например, 50): ", value_type=int,
                                      min_value=1)

    print("\nДоступные трансформации:")
    for idx, transform in enumerate(TRANSFORMATIONS):
        print(f"{idx}: {transform.__name__}")

    while True:
        selected_transforms = input("Введите номера трансформаций через запятую (например, 0,1,2): ")
        selected_transforms = selected_transforms.split(",")

        try:
            selected_transforms = [int(x.strip()) for x in selected_transforms]
            if all(0 <= x < len(TRANSFORMATIONS) for x in selected_transforms):
                break
            else:
                print("Ошибка: введите правильные номера трансформаций.")
        except ValueError:
            print("Ошибка: введите числа, разделённые запятыми.")

    transformations = [TRANSFORMATIONS[i] for i in selected_transforms]

    use_multithreading = input("\nХотите использовать многозадачность? (y/n): ").lower()
    use_multithreading = use_multithreading == "y"

    num_threads = 1
    if use_multithreading:
        num_threads = get_valid_input("Введите количество потоков (например, 4): ", value_type=int, min_value=1)

    return width, height, samples, iter_per_sample, transformations, use_multithreading, num_threads


def parallel_generate_fractal(image: FractalImage, world: Rect, transformations: list, samples: int,
                              iter_per_sample: int, symmetry: int, num_threads: int):
    """
    Параллельная генерация фрактала с использованием многозадачности.

    :param image: объект изображения
    :param world: мировая область
    :param transformations: список трансформаций
    :param samples: количество выборок
    :param iter_per_sample: количество итераций на выборку
    :param symmetry: симметрия фрактала
    :param num_threads: количество потоков для генерации
    """
    samples_per_thread = samples // num_threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(generate_fractal, image, world, transformations, samples_per_thread, iter_per_sample,
                            symmetry)
            for _ in range(num_threads)
        ]
        for future in futures:
            future.result()


def main():
    width, height, samples, iter_per_sample, transformations, use_multithreading, num_threads = user_input()

    world = Rect(-1.5, -1.5, 3, 3)
    image = FractalImage(width, height)
    print("Подождите, пожалуйста! Я рисую :)")

    if use_multithreading:
        parallel_generate_fractal(image, world, transformations, samples, iter_per_sample, symmetry=1,
                                  num_threads=num_threads)
    else:
        generate_fractal(image, world, transformations, samples, iter_per_sample)
    save_image(image, "fractal_flame.png")
    print("Изображение сохранено как fractal_flame.png")


if __name__ == "__main__":
    main()
