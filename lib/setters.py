#!/usr/bin/env python3

# == Save/Update functions ==
def save_user_selections(database_path: str, data: dict):
    #Append user data to a csv file, should only be new users.

    with open(f'{database_path}data.csv', 'a') as f:
        csv_line = ''
        #TODO 1. saved_selections = getUserSelections() # Get a list of saved selections to prevent double voting.
        for ip,v in data.items():
            # 2. if(ip in saved_selections): pass; else if()... basically dont let people double vote/select.
            if(type(v) == dict):
                # Append selection filenames to data.csv
                try:
                    sel_no_brackets = '' #str(v['selections'])[1:-1]
                    for i in v['selections']: sel_no_brackets += str(i)+','
                    sel_no_brackets = sel_no_brackets[:-1]
                    csv_line += f'{ip},{sel_no_brackets}\n'
                except KeyError as e:
                    print(f"{e} \nKey: {v}, not found.")
        f.write(csv_line)


def updateImageACL(database_path: str, userKey: str, imageName: str):
    # Db of who uploaded what image.
    #
    #userKey = User's IP
    with open(f'{database_path}imageACL.csv', 'a') as f:
        f.write(f'{userKey},{imageName}\n')
