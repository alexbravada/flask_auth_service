import os

import requests

from app import app

ROUTE_RULES = {
    'role': '/api/v1/auth/role',
    'user': '/api/v1/user',
    'userrole': '/api/v1/userrole'
}
API_STATIC_PATH = '/api/v1/auth'


def get_routes() -> dict[str:list[dict]]:
    '''
    return: {
        mark_route(role/user/...):[
            {path w/o api_static_path: instance Rule class with properties of current route}, {}, {}, ...
        ],
        mark_route:[...]
    }
    '''
    urlmap = app.url_map
    outdict = {key: list() for key in ROUTE_RULES.keys()}
    worklist = [x for x in urlmap.iter_rules()]
    for route in worklist:
        if '/static/' in route.rule:
            continue
        for key, value in ROUTE_RULES.items():
            if value in route.rule:
                mark_route = key
                break
        outdict[mark_route].append({route.rule.replace(API_STATIC_PATH, ''): route})
    return outdict


def main():
    print(get_routes())


if __name__ == '__name__':
    main()
