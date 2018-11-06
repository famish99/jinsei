#!/usr/bin/python3

from argparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader
from ruamel import yaml
from shutil import copyfile
from time import sleep, strftime
import subprocess
import sys
import traceback
import os


NUM_COLS = 3


def build_resume(args):
    os.makedirs('build', exist_ok=True)
    for f_name in os.listdir(args.template_dir):
        if '.css' in f_name:
            copyfile(
                os.path.join(args.template_dir, f_name),
                os.path.join('build', f_name)
                )
    env = Environment(loader=FileSystemLoader(args.template_dir))
    with open(args.input, 'r') as ifp:
        # Needed for cases file reports a modified time but changes are cached
        ifp.flush()
        context = yaml.load(ifp)
        template = env.get_template(context['template'])
        ir_path = os.path.join('build', 'out_%s' % context['template'])
        with open(ir_path, 'w') as ofp:
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
            ofp.write(template.render(context))
            ofp.flush()
        subprocess.run([
            'wkhtmltopdf',
            '-s', 'Letter',
            '--print-media-type',
            ir_path,
            args.output
            ])


def auto_build_resume(args):
    print('Watching for changes - %s' % args.input)

    def last_updated_time():
        return max(
            os.stat(args.input).st_mtime,
            *(
                os.stat(os.path.join(args.template_dir, filename)).st_mtime
                for filename in os.listdir(args.template_dir)
                if '.sw' not in filename
                )
            )

    last_updated = last_updated_time()
    try:
        build_resume(args)
        while True:
            if last_updated_time() != last_updated:
                last_updated = last_updated_time()
                print('rebuilding - %s' % strftime('%I:%M:%S'))
                try:
                    build_resume(args)
                except Exception:
                    traceback.print_exc(file=sys.stdout)
            sleep(5)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--template-dir', dest='template_dir', default='templates')
    parser.add_argument('--method', dest='method', choices=['once', 'auto'], default='once')
    args = parser.parse_args()

    (auto_build_resume if args.method == 'auto' else build_resume)(args)
