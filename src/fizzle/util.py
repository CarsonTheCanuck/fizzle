import os
import yaml
from datetime import datetime
import yamldown
from jinja2 import Environment, Template, FileSystemLoader
from .markdown import md

stage1_template = """
{%- if extends -%}
{% raw %}{%{% endraw %} extends '{{ extends }}' {% raw %}%}{% endraw %}
{%- endif %}
{% raw %}{% block page %}{% endraw %}
{{ source_code }}
{% raw %}{% endblock page %}{% endraw %}
"""


def traverse_folder(folder, path_list=[]):
    for filename in os.listdir(folder):
        fpath = os.path.join(folder, filename)
        if filename.startswith('_'):
            continue

        if os.path.isdir(fpath):
            path_list.append(filename)
            yield from traverse_folder(fpath, path_list)
        else:
            yield filename, path_list


def compile_file(jinja_env, filename, source_dir, destination_dir, path_list):
    path = '/'.join(path_list)
    name_extension = os.path.splitext(filename)

    if name_extension[1] == '.md':
        output_filename = f'{name_extension[0]}.html'
    else:
        output_filename = filename


    try:
        with open(os.path.join(source_dir, path, filename)) as stream:
            metadata, source_code = yamldown.load(stream)
    except UnicodeDecodeError:
        metadata = None

    if metadata:
        if name_extension[1] == '.md':
            source_code = md(source_code)

        stage1 = jinja_env.from_string(stage1_template).render(
            page=metadata,
            extends=metadata.get('template'),
            source_code=source_code
        )
        stage2 = jinja_env.from_string(stage1).render(page=metadata)
        
        with open(os.path.join(destination_dir, path, output_filename), 'w+') as wstream:
            wstream.write(stage2)
    else:
        path_so_far = destination_dir
        for part in path_list:
            path_so_far = os.path.join(path_so_far, part)
            if not os.path.exists(path_so_far):
                os.mkdir(path_so_far)
        with open(os.path.join(source_dir, path, filename), 'rb') as src_stream:
            with open(os.path.join(destination_dir, path, output_filename), 'wb+') as dest_stream:
                data = src_stream.read(512)
                while data != b'':
                    dest_stream.write(data)
                    data = src_stream.read(512)


def date(format):
    return datetime.now().strftime(format)


def build(source_dir, destination_dir):
    # TODO: blog post support
    try:
        with open(os.path.join(source_dir, '_config.yml')) as stream:
            config = yaml.safe_load(stream)
    except FileNotFoundError as ex:
        print(ex)
        print('No _config.yml found in source directory.')
        exit(1)
    except yaml.YAMLError:
        print('YAML syntax error in _config.yml.')
        exit(1)

    jinja_env = Environment(loader=FileSystemLoader(
        os.path.join(source_dir, '_templates')
    ))
    jinja_env.globals = {
        'site': config,
        'date': date
    }

    for filename, path_list in traverse_folder(source_dir):
        compile_file(jinja_env, filename, source_dir, destination_dir, path_list)

    
    