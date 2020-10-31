import os


def create_folders():
    if not os.path.exists('reportajes'):
        os.mkdir('reportajes')

    return True


def task_flake():
    return {
        'targets': ['reportajes/flake8.txt', 'src/'],
        'actions': [(create_folders, [], {}), 'flake8 --exit-zero --output-file=reports/flake8.txt src'],
        'clean': True
    }
    