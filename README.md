Data Science @ IFCA
===================

This portal gathers all Data Science and Deep Learning projects developed at IFCA. Live at [http://datascience.ifca.es/](http://datascience.ifca.es/) (mirror: [http://deep.ifca.es/](http://deep.ifca.es/))

To include a new project, add a YAML file to the `/projects` folder. You can use these files as templates to follow the syntax:
* [template for ongoing project](./deep_at_ifca/projects/template-ongoing.yaml)
* [template for ended project](./deep_at_ifca/projects/template-ended.yaml)

When adding `areas` or `tags` try to make them general enough so that they can be shared across more than one project. 
You can always check your YAML syntax with [YAMLlint](http://www.yamllint.com/).

To run the portal in debug mode use:
```bash
python main.py
```

To run the portal in production mode:
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```
