#!/usr/bin/python3
import argparse
from argparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader
from ruamel import yaml
from shutil import copyfile
from time import sleep, strftime
from typing import Any
import subprocess
import sys
import traceback
import os


NUM_COLS = 3


def parse_context(input_file: str, overrides: list[str]) -> dict[str, Any]:
    context: dict[str, Any] = {}
    with open(input_file, 'r') as ifp:
        # Needed for cases file reports a modified time but changes are cached
        ifp.flush()
        context.update(yaml.load(ifp, Loader=yaml.Loader))
    for override in overrides:
        with open(override, 'r') as ifp:
            # Needed for cases file reports a modified time but changes are cached
            ifp.flush()
            over_dict: dict[str, Any] = yaml.load(ifp, Loader=yaml.Loader)
            extensions: list[dict[str, str]]
            if extensions := over_dict.pop('skills', None):
                context['skills'].extend(extensions)
            if extensions := over_dict.pop('experience', None):
                context['experience'].extend(extensions)
            if extensions := over_dict.pop('education', None):
                context['education'].extend(extensions)
            if extensions := over_dict.pop('projects', None):
                context['projects'].extend(extensions)
            context.update(over_dict)
    return context


def build_resume(build_args: argparse.Namespace) -> None:
    os.makedirs('build', exist_ok=True)
    for f_name in os.listdir(build_args.template_dir):
        if '.css' in f_name:
            copyfile(
                os.path.join(build_args.template_dir, f_name),
                os.path.join('build', f_name)
            )
    context = parse_context(build_args.input, build_args.overrides)
    env = Environment(loader=FileSystemLoader(build_args.template_dir))
    template = env.get_template(context['template'])
    skill_len = len(context['skills'])
    skills = (
        context['skills'] + [
            ' '
            for _ in range(
                (skill_len % NUM_COLS) and
                NUM_COLS - (skill_len % NUM_COLS)
                )
            ]
        )
    context['skills'] = [skills[i::NUM_COLS] for i in range(NUM_COLS)]
    ir_path = os.path.join('build', 'out_%s' % context['template'])
    with open(ir_path, 'w') as ofp:
        ofp.write(template.render(context))
        ofp.flush()
    subprocess.run([
        'wkhtmltopdf',
        '-s', 'Letter',
        '--print-media-type',
        '--enable-local-file-access',
        ir_path,
        build_args.output
        ])


def auto_build_resume(build_args: argparse.Namespace) -> None:
    print('Watching for changes - %s' % build_args.input, file=sys.stderr)

    def last_updated_time() -> float:
        return max(
            os.stat(build_args.input).st_mtime,
            *(os.stat(override).st_mtime for override in build_args.overrides),
            *(
                os.stat(os.path.join(build_args.template_dir, filename)).st_mtime
                for filename in os.listdir(build_args.template_dir)
                if '.sw' not in filename
                )
            )

    last_updated = last_updated_time()
    try:
        build_resume(build_args)
        while True:
            if last_updated_time() != last_updated:
                last_updated = last_updated_time()
                print('rebuilding - %s' % strftime('%I:%M:%S'), file=sys.stderr)
                try:
                    build_resume(build_args)
                except Exception:
                    traceback.print_exc(file=sys.stderr)
            sleep(5)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--overrides', dest='overrides', nargs='*', default=[])
    parser.add_argument('--template-dir', dest='template_dir', default='templates')
    parser.add_argument('--method', dest='method', choices=['once', 'auto'], default='once')
    args = parser.parse_args()

    (auto_build_resume if args.method == 'auto' else build_resume)(args)
