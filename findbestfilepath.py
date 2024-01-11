import findclusterid
import getheighestrankedclient
import torch

from countmatchingfiles import read_matching_files


def find_best_file_path():
    contents1 = read_matching_files()
    highclientid = ""
    for clientid, file_path in contents1:
        clusterid = findclusterid.find_cluster_id(int(clientid))
        print(f'Hoogste clusterid in loop: {clusterid}')
        highclientid = getheighestrankedclient.get_highest_ranked_client(clusterid)
        print(f'Hoogste clientid in loop: {highclientid}')
        file_path = torch.load(file_path)
        break
    print(f'Hoogste clientid out loop: {highclientid}')

    bestfile_path = ""
    for clientid, file_path in contents1:
        print(clientid)
        print(highclientid)
        if int(clientid) == int(highclientid):
            print(file_path)
            bestfile_path = file_path
            break

    return bestfile_path
