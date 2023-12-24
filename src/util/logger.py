import os, sys, json
from datetime import datetime

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from util.file_master import add_content_in_file

def log_line(line):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dated_line = f'{now} : {line}\n'
    add_content_in_file('python.log', dated_line)

def log_line_in_debug(line, isJson):
    if "debug" in sys.argv:
        if isJson:
            log_line(f'DEBUG JSON :::\n {json.dumps(line, indent=2, ensure_ascii=False)}')
        else:
            log_line(f'DEBUG ::: {line}')

def log_line_json(line, isJson):
    if isJson:
        log_line(f'JSON :::\n {json.dumps(line, indent=2, ensure_ascii=False)}')