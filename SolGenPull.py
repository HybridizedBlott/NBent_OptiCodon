#Pull blast data from Sol Genomics Networks 

from splinter import Browser
from selenium.webdriver.common.keys import Keys 
import threading
import time
import argparse
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

parser = argparse.ArgumentParser(prog='SolGenBlast', description='Automates tblastn operations on the Sol Genomics Database given a protein fasta file')

parser.add_argument('-f', '--inputFile', required=True, help='Input file containg protein fasta sequences')
parser.add_argument('-t','--threads', default=1, help='Number of parallel processes to use')
parser.add_argument('-o', '--outputFile', required=True, help='Name of output file containing cDNA sequences')

args = parser.parse_args()

def ProteinFastaExtraction():
    sequences = []
    with open(args.inputFile, 'r') as f:
        current_seq = ""
        for line in f:
            if line.startswith('>'):
                if current_seq:
                    sequences.append(current_seq)
                current_seq = ""
            else:
                current_seq += line.strip()
        if current_seq: 
            sequences.append(current_seq)
        f.close()
    return sequences         

def SolBlast(seq):
    browser = Browser('chrome', headless=True)
    browser.visit('https://solgenomics.net/tools/blast/?db_id=330')
    browser.select('database', '266')
    browser.select('program_select', 'tblastn')
    browser.select('input_options', 'autodetect')
    browser.fill('sequence', seq)
    browser.find_by_id('submit_blast_button').click()
    time.sleep(20)
    browser.find_by_css('.blast_match_ident').first.click()
    time.sleep(10)
    first_match = browser.find_by_css('.match_details')
    browser.visit(first_match['href'])
    if browser.is_element_present_by_css('span.sequence', wait_time=20):
        sequence_element = browser.find_by_css('span.sequence')
        fasta = sequence_element.text
    else:
        print("No sequence element found!")
    browser.quit()

    return fasta

def WriteToDNAfile(fasta):
    with open(args.outputFile,'a') as f:
        f.write(f'{fasta}\n')
        f.close()

def pipeline(ProFasta, progress, task_id):
    for seq in ProFasta:
        try:
            fasta = SolBlast(seq)
            progress.update(task_id, advance=1)
            WriteToDNAfile(fasta)
        except:
            print(f'\n\nThe BLAST instance failed for the following sequence:\n{seq}\n')
            progress.update(task_id, advance=1)
            pass 

def data_split(thread:int = 1):
    data = {}
    ProFasta_size = len(ProteinFastaExtraction())
    for i in range(thread):
        data[i] = [x for x in range(i,ProFasta_size,thread)]
    
    return data

def main():
    print('\nNow running SolGen automated BLAST program')
    print(f'Input file name: {args.inputFile}')
    print(f'Output file name: {args.outputFile}\n')
    processes = int(args.threads)
    ProFasta = ProteinFastaExtraction()

    splits = data_split(processes)
    threads = []

    print(f'\nLaunching Search - Number of Threads = {processes}')
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        transient=True,
    ) as progress:
        if processes > 1:
            for data in splits:
                task_id = progress.add_task(f"Thread {data + 1}", total=len(splits[data]))
                t = threading.Thread(target=pipeline, args=([ProFasta[idx] for idx in splits[data]], progress, task_id))
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            task_id = progress.add_task("Processing sequences", total=len(ProFasta))
            pipeline(ProFasta, progress, task_id)
    
    print(f'Job Finished - Saved to {args.outputFile}')

if __name__ == "__main__":
    main()
