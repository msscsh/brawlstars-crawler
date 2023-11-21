from datetime import datetime

def log_line(line):
    with open('python.log', 'a') as log_file:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dated_line = f'{now} : {line}'
        log_file.write(f'{dated_line}\n')
        print(dated_line)