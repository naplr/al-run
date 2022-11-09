import os, sys

if __name__ == "__main__":
    target = sys.argv[1]
    outfilename = f'{target}/txlogs.csv'
    files = [f for f in os.listdir(target) if f.endswith('.csv')]
    with open (outfilename, 'w') as outfile:
        for f in files:
            with open(f'{target}/{f}') as infile:
                outfile.write(infile.read())