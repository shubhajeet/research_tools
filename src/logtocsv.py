#log_to_csv.py

import sys
import pandas as pd
import argparse

def logparser(logfile=sys.stdin, outfile=sys.stdout, fields=None):
    lines = logfile.read().split('\n')
    #print(lines)
    tokens = [l.split(" ") for l in lines]
    #print(tokens)
    csvdata = []
    for token in tokens:
        #print(token)
        row = {}
        for i in range(len(token)):
            if len(token[i]) == 0:
                continue
            if token[i][-1] == ":":
                key = token[i][:-1:]
                value = token[i+1]
                if fields == None or (fields != None and key in fields):
                    row[key] = value
        #print(row)
        csvdata.append(row)
    #csvdata = [{token[i][:-1]: token[i+1] for i in range(len(token)) if token[-1] == ':'} for token in tokens]
    #print(csvdata)
    df = pd.DataFrame(csvdata)
    #print(df)
    df.to_csv(outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("logtocsv","converts key: value in log file to a csv")
    parser.add_argument("--input",help="input log file",default=None)
    parser.add_argument("--output",help="output csv file",default=None)
    parser.add_argument("-f","--fields",nargs="+",help="list of fields to be filtered",default=None)
    args = parser.parse_args()
    input = sys.stdin
    output = sys.stdout
    if args.input:
        input = open(args.input,"r")
    if args.output:
        output = open(args.output,"w")
    logparser(input,output,args.fields)
