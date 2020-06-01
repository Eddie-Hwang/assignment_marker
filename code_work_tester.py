import re
import os
import glob
import argparse
import subprocess

from tqdm import tqdm
from multiprocessing import Pool

parser = argparse.ArgumentParser()
parser.add_argument('--multi', type=int, default=1)
parser.add_argument('--dir', type=str, default='./hw3')

def test_run(pyfile):
    student_no = re.search('[0-9]{8}', pyfile, re.IGNORECASE).group()
    student_path = os.path.join(os.path.dirname(pyfile), student_no)
    
    out_log_path = os.path.join(student_path, 'stdout.txt')
    err_log_path = os.path.join(student_path, 'stderr.txt')
    if not(os.path.exists(student_path)):
        os.makedirs(student_path)
        with open(out_log_path, 'w') as stdout, open(err_log_path, 'w') as stderr:
            subprocess.call(['python', pyfile], stdout=stdout, stderr=stderr)
    else:
        if os.path.getsize(err_log_path) > 0:
            with open(out_log_path, 'w') as stdout, open(err_log_path, 'w') as stderr:
                subprocess.call(['python', pyfile], stdout=stdout, stderr=stderr)

def get_err_stats(cur_dir):
    errs = list()
    for student_dir in glob.glob(os.path.join(cur_dir, '*/')):
        if os.path.getsize(os.path.join(student_dir, 'stderr.txt')) > 0:
            errs.append(re.search('[0-9]{8}', student_dir, re.IGNORECASE).group())
    
    return errs

def _main(args):
    pool = Pool(processes=args.multi)
    pyfiles = [x for x in glob.glob(os.path.join(args.dir, '*.py')) if re.search('[0-9]{8}', x, re.IGNORECASE)]
    with Pool(processes=args.multi) as p:
        with tqdm(total=len(pyfiles)) as pbar:
            for i, _ in enumerate(p.imap_unordered(test_run, pyfiles)):
                pbar.update()

    print('\n' + '-' * 50)
    for err_studentno in get_err_stats(args.dir):
        print(err_studentno)
    
    # pool.map(test_run, glob.glob(os.path.join(args.dir, '*.py')))
        
if __name__ == '__main__':
    _main(parser.parse_args())
