from abc import ABC, abstractmethod
import os
from pprint import pprint
import requests


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
        {'title': 'вакансия', 'url': 'ссылка на вакансию', 'salary min': 'минимальная зарплата', 'salary max': 'максимальная зарплата', 'requirement': 'основные требования'}"""
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
        {'title': 'вакансия', 'url': 'ссылка на вакансию', 'salary min': 'минимальная зарплата', 'salary max': 'максимальная зарплата', 'requirement': 'основные требования'}"""
        vacancies = hh_api.get_vacancies()
        new_json = []
        for i in vacancies['items']:
            try:
                d = {
                'title': i['name'],
                'url': i['url'],
                'salary min': i['salary']['from'],
                'salary max': i['salary']['to'],
                'requirement': i['snippet']['requirement']
                }
            except(TypeError,IndexError, ValueError, KeyError):
                d = {
                    'title': i['name'],
                    'url': i['url'],
                    'salary min': 0,
                    'salary max': 0,
                    'requirement': i['snippet']['requirement']
                }
            else:
                if not i['salary']['from'] or not i['salary']['to']:
                    d = {
                        'title': i['name'],
                        'url': i['url'],
                        'salary min': 0,
                        'salary max': 0,
                        'requirement': i['snippet']['requirement']
                    }
            new_json.append(d)
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
        {'title': 'вакансия', 'url': 'ссылка на вакансию', 'salary min': 'минимальная зарплата', 'salary max': 'максимальная зарплата', 'requirement': 'основные требования'}"""
        vacancies = sj_api.get_vacancies()
        new_json = []
        for i in vacancies['objects']:
            try:
                d = {
                'title': i['profession'],
                'url': i['link'],
                'salary min': i['payment_from'],
                'salary max': i['payment_to'],
                'requirement': i['candidat']
                }
            except(TypeError, IndexError, ValueError, KeyError):
                d = {
                    'title': i['profession'],
                    'url': i['link'],
                    'salary min': 0,
                    'salary max': 0,
                    'requirement': i['candidat']
                }
            else:
                if not i['payment_from'] or not i['payment_to']:
                    d = {
                        'title': i['profession'],
                        'url': i['link'],
                        'salary min': 0,
                        'salary max': 0,
                        'requirement': i['candidat']
                    }
            new_json.append(d)
        return new_json

