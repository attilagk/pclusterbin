#! /usr/bin/env python3
import synapseclient
import subprocess
import os
import pandas as pd

chess_s3_bucket = 's3://chesslab-bsmn'
efs_dirpath = '/efs/alignments'

def synlogin():
    syn = synapseclient.login()
    return(syn)

def getfromscratch(synID, dirpath, syn):
    e = syn.get(synID, downloadLocation=dirpath)
    return(e)

def efs2s3(fpath, s3prefix='alignments/'):
    l = ['aws', 's3', 'cp', fpath, chess_s3_bucket + '/' + s3prefix]
    p = subprocess.run(l)
    return(p)

def transfer(synID, syn):
    e = getfromscratch(synID, dirpath=efs_dirpath, syn=syn)
    p = efs2s3(fpath=e.path, s3prefix='alignments/')
    if p.returncode == 0:
        os.remove(e.path)
    return(p)

def getsynIDs(folderID='syn20735395'):
    syn = synapseclient.login()
    folder = syn.get(folderID)
    synIDs = [e['id'] for e in syn.getChildren(folder)]
    names = [e['name'] for e in syn.getChildren(folder)]
    val = pd.Series(data=synIDs, index=names)
    return(val)

def transferall(synIDs, syn):
    l = list(synIDs)
    ps = [transfer(y, syn) for y in l]
    return(ps)
