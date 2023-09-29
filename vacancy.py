class Vacancy:

    def __init__(self, title: str, url: str, salary_min: int, salary_max: int, requirement: str):
        """Инициализирует экземпляры класса"""
        self.title = title
        self.url = url
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.requirement = requirement

    def __repr__(self):
        """Возвращает печатную форму экземпляра класса"""
        return f'Вакансия: {self.title}\n' \
               f'Ссылка на вакансию: {self.url}\n' \
               f'Зарплата: от {self.salary_min} до {self.salary_max}\n' \
               f'Описание вакансии: {self.requirement}\n'

    def __str__(self):
        """Возвращает печатную форму экземпляра класса"""
        return f'Вакансия: {self.title}\n' \
               f'Ссылка на вакансию: {self.url}\n' \
               f'Зарплата: от {self.salary_min} до {self.salary_max}\n' \
               f'Описание вакансии: {self.requirement}\n'

    def __ge__(self, other):
        return self.salary_min >= other.salary_min

    def __le__(self, other):
        return self.salary_min <= other.salary_min

    def validate_data(self):
        """
        Функция для валидации данных
        """
        if self.title is None:
            self.title = ' '
        elif self.url is None:
            self.url = ' '
        elif self.salary_min is None:
            self.salary_min = 0
        elif self.salary_max is None:
            self.salary_max = 0
        elif self.requirement is None:
            self.requirement = ' '
