#!/usr/bin/env python

import feedparser
import codecs
from dateutil.parser import parse
import constants as c

def parse_feeds():
    with open(c.feed_path, 'r') as f:
       for eachline in f:
            # Get the feed.
            feed = feedparser.parse(eachline)
            if feed is None:
                continue

            # It's possible the feed exists, but it's empty.
            try:
                print(feed['channel']['title'])
                feed_title = feed['channel']['title']
            except KeyError:
                print(str(feed['channel']) + " exists but is EMPTY!")
                continue

            # Replace any odd characters in the feed title.
            feed_title = feed_title.replace('/', '-')
            feed_title = feed_title.replace("&#039;", "'")

            # Using the name of the feed, get the file in which this feed's 
            # entries are stored. Read only the first line, as this will 
            # have the latest entry.
            d = codecs.open(c.feeds_dir + feed_title, 
                            encoding='utf-8', 
                            mode='a+')
            first_line = d.readline()
        
            # It could be that this is a new feed, in which case there won't 
            # be any entries in the feed's file. Empty strings are 'falsy' in
            # Python, meaning they're considered false in a Boolean context.
            if not first_line:
                file_date = 0
            else:
                file_date = ' '.join(first_line.split(' ')[:1])

            for i in range(0, len(feed['entries'])):
                entry = feed['entries'][i]
                feed_date = parse(entry.published).strftime('%s')
				
                if int(feed_date) > int(file_date):
                    d.write("%s %s %s %s\n" % (feed_date, 
                                               "NEW", 
                                               entry.title, 
                                               entry.link))
            d.close()

            # Sort the file we just wrote. The encoding should be correct,
            # so just open as normal.
            with open(c.feeds_dir + feed_title, "r+") as d:
                all_lines = d.readlines()
                d.seek(0)
                all_lines.sort(key=lambda l: int(l.split()[0]), reverse=True)
                for i in all_lines:
                    d.write(i)
                d.truncate()

parse_feeds()
