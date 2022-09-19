# Copyright (c) 2020 Spanish National Research Council
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pathlib
import re

from markdown import markdown
import pandas as pd
import yaml


maindir = pathlib.Path(__file__).resolve().parent


def load_projects():
    """
    Load projects from YAML files
    """
    keys = []
    projects = {}
    for p in (maindir / 'projects').iterdir():
        if p.stem.startswith('template-'):
            continue
        try:
            with open(p, 'r') as f:
                pname = p.stem.replace(' ', '')
                data = yaml.safe_load(f)

                data['snippet'] = data['description']
                data['snippet'] = data['snippet'].split(' ')
                data['snippet'] = ' '.join(data['snippet'][:15]) + ' [...]' # keep first 15 words
                data['snippet'] = re.sub('\[([\w\s\d]+)\]\(([\w\d/:./?=#]+)\)', r'\1', data['snippet'])  # replace markdown links
                data['snippet'] = data['snippet'].replace('_', '').replace('*', '')  # replace bold and italics

                data['description'] = markdown(data['description'])   # convert to html
                projects[pname] = data
                keys.append([data['end'], data['start'], pname])
        except Exception as e:
            print(f'Error loading {p}')
            print(e)

    # Sort
    keys = pd.DataFrame(keys, columns=['end', 'start', 'name'])
    keys = keys.sort_values(['end', 'start', 'name'],
                            ascending=[False, False, True])
    sorted_projects = {}
    for k in keys['name']:
        sorted_projects[k] = projects[k]

    return sorted_projects


def get_filters(projects):
    """
    Get filter values based on projects
    """
    filters = {}
    areas, tags = [], []
    for p in projects.values():
        if 'areas' in p.keys():
            areas += p['areas']
        if 'tags' in p.keys():
            tags += p['tags']
    filters['areas'] = sorted(list(set(areas)))
    filters['tags'] = sorted(list(set(tags)))
    return filters


def project_check(p, user_args, mode='and'):
    """
    Check if project satisfies user filter
    mode=and: project satisfies all conditions
    mode=any: project satisfies any of the conditions
    """

    p_args = []
    if 'areas' in p.keys():
        p_args += [f'area-{i}' for i in p['areas']]
    if 'tags' in p.keys():
        p_args += [f'tag-{i}' for i in p['tags']]
    if (p['end'] == 'ongoing'):
        p_args += ['ongoing']
    p_args = set(p_args)

    intset = p_args.intersection(user_args)
    if mode == 'and':
        if intset == user_args:
            return True
    if mode == 'or':
        if len(intset) != 0:
            return True
    return False


def filter_projects(args, projects):
    """
    Filter projects according to user selected values
    """
    keys = set(args.keys())
    projs = {}
    for pk, pv in projects.items():
        if project_check(pv, keys):
            projs[pk] = pv
    return projs
