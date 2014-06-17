#!/usr/bin/env python

import os
import datetime
import constants as c
import re

# The contents of the table.
HEADING = '<b>%s</b></br>'
TITLE_PODCAST = HEADING % "Podcasts"
TITLE_MUSIC = HEADING % "Music"
TITLE_APP_STATS = HEADING % "App Stats"
TITLE_WORDS = HEADING % "Words"

# The attributes of the table.
TABLE_OPEN = '<table>'
TABLE_CLOSE = '</table>'
TABLE_ROW_OPEN = '<tr>'
TABLE_ROW_CLOSE = '</tr>'
TABLE_DATA_OPEN = '<td valign="top">'
TABLE_DATA_CLOSE = '</td>'
TABLE_COL_WIDTH = '<col width="130">'

# The CSS of the table.
BORDER =     """<style> 
                table,th,td {
                    border:1px solid black;
                    border-collapse:collapse
                }
                </style>"""
ELIP =       """<style>
                a {
                    display:inline-block;
                    white-space:nowrap; 
                    max-width:90%; 
                    overflow:hidden;
                    text-overflow:ellipsis; 
                    text-decoration:none;
                 }
                 </style>""" 

LINK = ' <a href="/goto?line=%s&dir=%s" target="_blank">%s</a></br>'

LINES_PER_FEED = 2

def table_style(f):
    f.write(BORDER)
    f.write(ELIP)
    return

def create_html():
    f = open(c.template_path, 'w')

    # Make the table look nice.
    table_style(f)

    for filename in os.listdir(c.feeds_dir):
        if os.path.isfile(os.path.join(c.feeds_dir, filename)):
            head = False
            count = 0
            d = open(os.path.join(c.feeds_dir, filename), 'r')
            for line in d:            
                if count < LINES_PER_FEED:
                    if 'NEW' in line:
                        count += 1
                        if not head:
                            f.write(HEADING % filename)
                            head = True
                        date = datetime.datetime.fromtimestamp(
                          int(line.split(' ', 1)[0])).strftime('%b %d')

                        # Sometimes a feed won't set the title for a given entry.
                        # Check for an empty title, and replace with placeholder.
                        title = ' '.join(line.split(' ')[2:-1])

                        # "title" is a string. Empty strings are 'falsy', so 
                        # Boolean handling applies. (Careful though - lots 
                        # of other things can be false.)
                        if not title:
                            title = '"No title provided - link is here"'

                        # Create overall line to write to the 'new entries' file.
                        string = LINK % (line.split(' ', 1)[0], 
                                         filename.replace('&', '%26'),                                         
                                         title)
                        f.write(date + string)
                else:
                    break
            d.close() 
    f.close()

create_html()
