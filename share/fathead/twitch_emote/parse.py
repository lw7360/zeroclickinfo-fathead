#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, os, glob, json


class TwitchEmoteItem:
  def __init__(self, name, imgid, imgurl, abstract):
    self.name = name
    self.imgid = imgid
    self.imgurl = imgurl
    self.abstract = abstract

  def __str__(self):
    fields = [ "twitch emote %s" % self.name,  #title
               "A", #type
               "",
               "",
               "gaming",  #categories
               "",
               "",
               "",
               "https://twitchemotes.com/emote/%s" % self.imgid,  #external_links
               "",
               self.imgurl,  #images
               self.abstract,  #abstract
               "https://twitchemotes.com"
             ]

    output = "%s\n" % ("\t".join(fields))
    return output


if __name__ == "__main__":
    # setup logger
    logging.basicConfig(level=logging.INFO,format="%(message)s")
    logger = logging.getLogger()
    
    # dump config items
    count = 0
    with open("output.txt", "wt") as output_file:
        for filepath in glob.glob('download/*'):
            with open(filepath, 'r') as f:
                data = json.loads(f.read())
                url = data['template']['large']
                if 'emotes' in data: # global.json
                    for key, value in data['emotes'].items():
                        imgid = str(value['image_id'])
                        imgurl = url.replace('{image_id}', imgid)
                        abstract = value['description'] if value['description'] else ''
                        item = TwitchEmoteItem(key, imgid, imgurl, abstract)

                        count += 1
                        output_file.write(str(item))
                        
                else: # subscriber.json
                    channels = data['channels']
                    url = data['template']['large']
                    for _, value in channels.items():
                        for emote in value['emotes']:
                            imgid = str(emote['image_id'])
                            imgurl = url.replace('{image_id}', imgid)
                            item = TwitchEmoteItem(emote['code'], imgid, imgurl, '')

                            count += 1
                            output_file.write(str(item))
                    
    logger.info("Parsed %d Twitch Emotes successfully" % count)
