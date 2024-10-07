import requests

GITLAB_ACCESS_TOKEN = 'REPLACE_ME'
GITLAB_URL = 'REPLACE_ME'
GROUP_ID = 'REPLACE_ME'


def get_headers():
    return {
        'Private-Token': GITLAB_ACCESS_TOKEN
    }


def get_subgroups(group_id):
    url = f'{GITLAB_URL}/api/v4/groups/{group_id}/subgroups'

    response = requests.get(url, headers=get_headers())
    response.raise_for_status()

    return response.json()


def get_projects(group_id):
    url = f'{GITLAB_URL}/api/v4/groups/{group_id}/projects'

    response = requests.get(url, headers=get_headers())
    response.raise_for_status()

    return response.json()


def print_tree_structure(group_id, prefix=''):
    subgroups = get_subgroups(group_id)
    projects = get_projects(group_id)

    for i, project in enumerate(projects):
        connector = '└── ' if i == len(projects) - 1 and not subgroups else '├── '
        print(f'{prefix}{connector}Project: {project["name"]}')

    for i, subgroup in enumerate(subgroups):
        connector = '└── ' if i == len(subgroups) - 1 else '├── '
        print(f'{prefix}{connector}Subgroup: {subgroup["name"]}')
        new_prefix = prefix + ('    ' if i == len(subgroups) - 1 else '│   ')
        print_tree_structure(subgroup['id'], new_prefix)


if __name__ == '__main__':
    print(f'Group: {GROUP_ID}')
    print_tree_structure(GROUP_ID)
