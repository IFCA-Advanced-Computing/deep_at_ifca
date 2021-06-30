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

from flask import Flask, render_template, request

import utils


app = Flask(__name__)
projects = utils.load_projects()
filters = utils.get_filters(projects)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        projs = utils.filter_projects(request.values.to_dict(),
                                      projects)
    else:
        projs = projects
    return render_template('home.html',
                           filters=filters,
                           projects=projs)


@app.route('/projects/<name>', methods=['GET'])
def project(name):
    return render_template('project.html',
                           project=projects[name])


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
