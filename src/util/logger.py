import sys, json
from datetime import datetime

def log_line(line):
    with open('python.log', 'a') as log_file:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dated_line = f'{now} : {line}'
        log_file.write(f'{dated_line}\n')
        print(dated_line)

def log_line_in_debug(line, isJson):
    if "debug" in sys.argv:
        if isJson:
            log_line(f'DEBUG JSON :::\n {json.dumps(line, indent=2, ensure_ascii=False)}')
        else:
            log_line(f'DEBUG ::: {line}')