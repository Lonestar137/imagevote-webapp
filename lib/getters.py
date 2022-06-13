#!/usr/bin/env python3
from os import listdir
from os.path import isfile, join


# == Get functions ==
def getFiles(path: str)->list[str]:
    #Return string list of files in a dir.
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def getUserSelections()->dict:
    #TODO Reads a csv file and returns it as dict.
    #Schema: {ip(col0): [col1, col2, col3, ...]}
    return {}
