import os
import sys
import re

IGNORE_FILES = ['tmp', 'wiki_processed.txt']
path_base = re.sub(r'\/$', '', sys.argv[1])
paths = [p for p in os.listdir(path_base) if p not in IGNORE_FILES]

def create_tmp_dir(path):
    directory = '{}/tmp'.format(path)
    try:
        os.mkdir(directory)
    except:
        pass

def process_text(text):
    processed = re.sub(r'<[^>]+>\n', '', text)
    processed = re.sub(r'((\[\[)|(\]\]))', '', processed)
    processed = re.sub(r'(\|)', r' \1 ', processed)
    return re.sub(r'\n+', '\n', processed)

first = True

for path in paths:
    current_path = '{}/{}'.format(path_base, path)
    files = [ f for f in sorted(os.listdir(current_path)) if f not in IGNORE_FILES ]
    create_tmp_dir(current_path)

    for f in files:
        with open('{}/{}'.format(current_path, f), 'r') as data:
            processed_text = process_text(data.read())

            with open('{}/tmp/{}.txt'.format(current_path, path), 'w') as out_file:
                out_file.write(processed_text)

    with open('{}/wiki_processed.txt'.format(path_base), 'w') as out_file:
        with open('{}/tmp/{}.txt'.format(current_path, path), 'r') as processed_file:
            start = '\n' if not first else ''
            out_file.write(start + processed_file.read())
    
    first = False