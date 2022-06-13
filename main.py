#!/usr/bin/env python3
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio import *

from os import listdir
from os.path import isfile, join

from decouple import config

# Custom
from lib.getters import *
from lib.setters import *
from lib.delete import *

def checkUnique(form_group):
    #Simple check to make sure select form submission is unique.
    #Checks a 1 layer k,v dictionary for redundant values.

    for key in list(form_group.keys()):
        if(form_group[key] == None):
            continue
        elif(key == 'upload_image'):
            continue
        elif(form_group[key] == 0 and form_group['s2'] == 0 and form_group['s3'] == 0):
            break

        for other_key in list(form_group.keys()):
            if(form_group[key] == form_group[other_key] and key != other_key):
                return(key, 'Cannot select the same option more than once.')


# == main ==
def main():
    shirt_image_dir = config('SHIRT_DIR') # Read .env file, get value of '' variable.
    database_path = './data/'

    #Renders content
    with use_scope('Main'): # use_scope creates a scope group for your pywebio objects.
        put_markdown('# Shirt selection')

        shirts = getFiles(shirt_image_dir) # Get list of image filenames.
        options = []
        for i, shirt in enumerate(shirts):
            put_markdown('## Option {}'.format(i))
            put_image(open(f'{shirt_image_dir}{shirt}', 'rb').read())

            options.append(i)

        collected_inputs = {}
        if(len(options) < 3):
            # if less than 3 pics uploaded only allow for uploads.
            collected_inputs = input_group('Voting will start after at least 3 images uploaded.', [
                file_upload(label='Upload your image', accept='image/*', name='upload_image')
            ], validate=checkUnique)
        else:
            #TODO if(info.user_ip inside csv file then dont show selections): only show upload option
            collected_inputs = input_group('', [
                select("Selection 1/3", options, name='s1'),
                select("Selection 2/3", options, name='s2'),
                select("Selection 3/3", options, name='s3'),
                file_upload(label='Upload your image', accept='image/*', name='upload_image')
            ], validate=checkUnique)

        sel = [] # list of form values for the each person, used to create csv row.
        for i in list(collected_inputs.keys()):
            if(collected_inputs[i] != None and i != 'upload_image'):
                image_name = shirts[collected_inputs[i]]
                sel.append(image_name)

        user_info = {
            info.user_ip: {
                'selections':sel,
                'agent': info.user_agent,
                'origin': info.origin,
                        }
        }

        # Finally save data
        if(collected_inputs['s1'] != 0 and collected_inputs['s2'] != 0 and collected_inputs['s3'] != 0): # If
            save_user_selections(database_path, user_info)

        pic = collected_inputs['upload_image']
        if(pic != None):
            with open(shirt_image_dir+pic['filename'], 'wb') as f:
                f.write(pic['content'])
                updateImageACL(database_path, info.user_ip, pic['filename'])
            put_markdown("### Refresh to see changes.")

    #STRETCH -- refresh the page after upload






if __name__ == '__main__':
    start_server(applications=main, port=8080, debug=True, )
