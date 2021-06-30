Deep @ IFCA
===========

This portal gathers all Deep Learning projects developed at IFCA.

To include a new project, add a YAML file to the `/projects` folder. You can use these files as templates to follow the syntax:
* [template for ongoing project](./deep_at_ifca/projects/template-ongoing.yaml)
* [template for ended project](./deep_at_ifca/projects/template-ended.yaml)

You can always check your YAML syntax with [YAMLlint](http://www.yamllint.com/)

To run the portal in debug mode use:
```bash
python main.py
```

To run the portal in production mode:
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```
