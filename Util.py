def storegroups():
    import pickle
    tracklist = []

    # tracklist [group, # number of times selected, [clientid]]
    # tracklist [[["2", 1], ["0"]], [["3", 0], ["1"]], [["4", 0], ["2"]], [["2", 1], ["3"]]]

    # Dict['Dict1']['name'] = 'Bob'

    with open('GroupClient.csv', 'r') as file:
        header = next(file)  # if there is a header
        for row in file:
            tracklist.append([[row[2], 0], [row[0]]])
    pickle.dump(tracklist, open("tracklist.p", "wb"))

def readtracklist():
    import pickle

    # Opening JSON file
    file = pickle.load(open("tracklist.p", "rb"))
    print(f'{file} OKEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEe')
    return file

def selectgroup():
    group = {}
    text = readtracklist()
    for row in text:
        print(row)
        for timesgroupselected in row:
            if len(timesgroupselected) > 1:
                # print(timesgroupselected)
                if not bool(group):
                    group[timesgroupselected[0]] = timesgroupselected[1]
                    print(group)
                else:
                    key = list(group.keys())[0]
                    # print(key)
                    # print(timesgroupselected)
                    if int(group[str(key)]) > int(timesgroupselected[1]):
                        print(int(group[str(key)]), int(timesgroupselected[1]))
                        group = {}
                        group[timesgroupselected[0]] = timesgroupselected[1]
    return group

def getclientsingroup():
    text = readtracklist()
    group = selectgroup()
    print(group)
    print(text)
    # getclientsingroup
    clients = []
    for row in text:
        if row[0][0] == list(group.keys())[0]:
            print(row[1][0])
            clients.append(row[1][0])
    updateclientgroup(group)
    return clients

def updateclientgroup(group):
    import json
    import pickle
    text = readtracklist()
    # update counter clientgroup
    for row in text:
        if row[0][0] == list(group.keys())[0]:
            row[0][1] = row[0][1] + 1
    pickle.dump(text, open("tracklist.p", "wb"))
    print(text)

