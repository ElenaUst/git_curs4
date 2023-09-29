from abc import ABC, abstractmethod
import os
import requests
from vacancy import Vacancy


API_hh = "https://api.hh.ru/vacancies"
API_sj: str = os.getenv('API_sj')


class APIVacancy(ABC):
    """Абстрактный класс для работы с сайтами вакансий"""

    @abstractmethod
    def get_vacancies(self) -> dict:
        """Получает список вакансий"""
        pass

    @abstractmethod
    def format_vacancies(self) -> dict:
        """Приводит полученные по API данные к единому формату:
        {'title': 'вакансия', 'url': 'ссылка на вакансию', 'salary_min': 'минимальная зарплата',
        'salary_max': 'максимальная зарплата', 'requirement': 'основные требования'}"""
        pass


class HHAPI(APIVacancy):
    """Класс для работы с сайтом HeadHunter"""

    def __init__(self, keytext, page=0):
        self.url = API_hh
        self.params = {
            'text': keytext,
            'page': page,
            'per_page': 10
        }

    def get_vacancies(self) -> dict:
        """Получает список вакансий"""
        vacancies = requests.get(self.url, params=self.params).json()
        return vacancies

    def format_vacancies(self):
        """Приводит полученные по API данные к единому формату:
        {'title': 'вакансия', 'url': 'ссылка на вакансию', 'salary_min': 'минимальная зарплата',
        'salary_max': 'максимальная зарплата', 'requirement': 'основные требования'}"""
        vacancies = self.get_vacancies()
        new_json = []
        for i in vacancies['items']:
            try:
                filtered_vacancies = {
                  'title': i['name'],
                  'url': i['url'],
                  'salary_min': i['salary']['from'],
                  'salary_max': i['salary']['to'],
                  'requirement': i['snippet']['requirement']
                }
            except(TypeError, IndexError, ValueError, KeyError):
                filtered_vacancies = {
                    'title': i['name'],
                    'url': i['url'],
                    'salary_min': 0,
                    'salary_max': 0,
                    'requirement': i['snippet']['requirement']
                }
            else:
                if not i['salary']['from'] or not i['salary']['to']:
                    filtered_vacancies = {
                        'title': i['name'],
                        'url': i['url'],
                        'salary_min': 0,
                        'salary_max': 0,
                        'requirement': i['snippet']['requirement']
                    }
            vac = Vacancy(**filtered_vacancies)
            new_json.append(vac)
        return new_json


class SuperJobAPI(APIVacancy):
    """Класс для работы с сайтом SuperJob"""

    def __init__(self, keytext, page=0):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.params = {
            'keyword': keytext,
            'page': page,
            'per_page': 10
        }

    def get_vacancies(self) -> dict:
        """Получает список вакансий"""
        headers = {'X-Api-App-Id': API_sj}
        vacancies = requests.get(self.url, headers=headers, params=self.params).json()
        return vacancies

    def format_vacancies(self):
        """Приводит полученные по API данные к единому формату:
        {'title': 'вакансия', 'url': 'ссылка на вакансию', 'salary_min': 'минимальная зарплата',
        'salary_max': 'максимальная зарплата', 'requirement': 'основные требования'}"""
        vacancies = self.get_vacancies()
        new_json = []
        for i in vacancies['objects']:
            try:
                filtered_vacancies = {
                  'title': i['profession'],
                  'url': i['link'],
                  'salary_min': i['payment_from'],
                  'salary_max': i['payment_to'],
                  'requirement': i['candidat']
                }
            except(TypeError, IndexError, ValueError, KeyError):
                filtered_vacancies = {
                    'title': i['profession'],
                    'url': i['link'],
                    'salary_min': 0,
                    'salary_max': 0,
                    'requirement': i['candidat']
                }
            else:
                if not i['payment_from'] or not i['payment_to']:
                    filtered_vacancies = {
                        'title': i['profession'],
                        'url': i['link'],
                        'salary_min': 0,
                        'salary_max': 0,
                        'requirement': i['candidat']
                    }
            vac = Vacancy(**filtered_vacancies)
            new_json.append(vac)
        return new_json
