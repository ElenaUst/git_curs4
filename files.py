import json
from abc import ABC, abstractmethod



class FileManager(ABC):
    """Класс для работы с файлами"""

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def read(self):
        """Чтение из файла"""
        pass

    @abstractmethod
    def write(self, vacancies):
        """Запись в файл"""
        pass


class JSONFileManager(FileManager):
    def __init__(self, filename):
        self.filename = filename + '.json'

    def get_vacancies(self):
        pass

    def read(self):
        """Переопределяем метод чтения из файла"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            json_data = json.loads(file.read())
            return json_data

    def write(self, vacancies):
        """Переопределяем метод записи в файл"""
        data = self.data_to_json(vacancies)
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))

    @staticmethod
    def data_to_json(vacancies):
        """"""
        vacancies_list = []
        for vacancy in vacancies:
            vacancy_dict = {
                'title': vacancy.title,
                'url': vacancy.url,
                'salary_min': vacancy.salary_min,
                'salary_max': vacancy.salary_max,
                'requirement': vacancy.requirement
            }
            vacancies_list.append(vacancy_dict)
        return vacancies_list

    def delete_vacancy(self, vacancies):
        """Удаление из файла"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            data_to_delete = file.read()
        data = json.loads(data_to_delete)
        vacancies_to_delete = self.data_to_json(vacancies)
        for vac in data:
            if vac in vacancies_to_delete:
                data.remove(vac)
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))

    def get_vacancies_by_keyword(self, keyword: int):
        """
        Переопределяем метод для получения вакансий по ключевому слову
        :param keyword: словарь с ключевыми словами для поиска
        :return list_of_vac: список вакансий, выбранных по ключевым словам
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            data_for_filter = file.read()
        data = json.loads(data_for_filter)
        list_of_vac = []
        for vacancy in data:
            if keyword == 'salary_input':
                if vacancy['salary_min'] < keyword:
                    list_of_vac.append(vacancy)
                    break
        return list_of_vac

    def get_list_vacancies(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            data_for_filter = file.read()
        data = json.loads(data_for_filter)
        return data
