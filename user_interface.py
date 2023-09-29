from api import HHAPI, SuperJobAPI
from files import JSONFileManager


def get_vacancies(api_manager):
    vacancies = []
    for api in api_manager:
        vacancies.extend(api.format_vacancies())
    return vacancies


def get_top_vacancies(json_file, choose_action_n):
    """
    Функция для получения вакансий, отсортированных по зарплате
    """
    vacancy_list = json_file.read()
    sorted_vacancies = sorted(vacancy_list, key=lambda el: el.get('salary_min'), reverse=True)[:choose_action_n]
    return sorted_vacancies


def actions_with_vacancies(json_file):
    """
    Функция, которая предлагает пользователю выбрать действие
    и получает ответы пользователя
    """
    print('Выберите действие, которое необходимо выполнить: ')
    print('1 - Получить топ N вакансий по зарплате\n'
          '2 - Получить вакансии с фильтрацией по зарплате\n'
          '3 - Удаление вакансии по критерию\n'
          '0 - Выйти из программы\n')
    while True:
        choose_action = input()
        if choose_action in ('1', '2', '3', '0'):
            if choose_action == '1':
                print('Введите количество вакансий для вывода топ N: ')
                choose_action_n = int(input())
                top_n = get_top_vacancies(json_file, choose_action_n)
                for vac in top_n:
                    print(vac)
                break
            elif choose_action == '2':
                salary_input = int(input("Введите минимальную зарплату: "))
                min_salary = json_file.get_vacancies_by_keyword({'salary_input': salary_input})
                for vac in min_salary:
                    print(vac)
                break
            elif choose_action == '3':
                low_salary_input = int(input("Введите критерий(минимальную зарплату) для удаления: "))
                json_file.delete_vacancy(json_file.get_vacancies_by_keyword(low_salary_input))
                print(f'Вакансии удалены из файла по критерию: {low_salary_input}')
                break
            else:
                print('До встречи!')
                break
        else:
            print('Некорректный ввод:\n')


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    while True:
        vacancy = []
        choose_platforms = input(
            'Выберите платформу для поиска вакансий:\n1 - HeadHunter\n2 - SuperJob\n3 - HeadHunter и SuperJob\n')
        if choose_platforms in ('1', '2', '3'):
            search_query = input('Введите название вакансии для поиска: \n')
            if choose_platforms == '1':
                hh = HHAPI(search_query)
                vacancy.append(hh)
                break
            elif choose_platforms == '2':
                sj = SuperJobAPI(search_query)
                vacancy.append(sj)
                break
            else:
                hh = HHAPI(search_query)
                sj = SuperJobAPI(search_query)
                vacancy.append(hh)
                vacancy.append(sj)
                break
        else:
            print("\nНекорректный ввод, попробуйте еще раз:\n")
    json_file = JSONFileManager('json_vacancies')
    json_file.write(get_vacancies(vacancy))
    actions_with_vacancies(json_file)

