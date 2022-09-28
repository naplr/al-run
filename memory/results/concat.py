import os

outfilename = 'logs/txlogs.csv'
files = [f for f in os.listdir('logs') if f.endswith('.csv')]
with open (outfilename, 'w') as outfile:
    for f in files:
        with open(f'logs/{f}') as infile:
            outfile.write(infile.read())
