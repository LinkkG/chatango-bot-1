#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########
# Imports #
###########

import megach
import config

import random

import os, sys
import xml, json
import urllib.request as urlreq, urllib.parse as urlparse

#########
# Start #
#########

class online_defs:

  apis = {"google_apis": "PUT_YOUR_API_KEY_HERE",
          "cx": "PUT_YOUR_CX_KEY_HERE"}

# https://developers.google.com/youtube/v3/getting-started # Create your yt 
# https://cse.google.com/cse - Create your cx
# https://developers.google.com/custom-search/v1/overview - Create your cs for gis in proyect main of yt

  def youtube(lang, p_video: str = ""):
      try:
        lang     = config.database.take_lang_user( lang, "youtube_answer" )
        video    = urlparse.quote( p_video.replace( " ", "+" ) )
        url      = ( "https://www.googleapis.com/youtube/v3/"
                    "search?q=/{}&part=snippet&key={}" ).format( video, online_defs.apis["google_apis"] )
        with urlreq.urlopen( url ) as open_url:
          decode   = open_url.read().decode("utf-8")
          data     = json.loads( decode )
          obtained = []
          if data["pageInfo"]["totalResults"] is not 0:
            for x in data["items"]:
              if "videoId" in x["id"]:
                obtained.append( x )
            video       = obtained[0]
            video_info  = video["snippet"]
            video_id    = video["id"]["videoId"]
            link        = "http://www.youtube.com/watch?v={}".format( video_id )
            title       = video_info["title"]
            upload_by   = video_info["channelTitle"]
            description = video_info["description"] if video_info["description"] else "N/A"
            text        = lang[0]
            return text.format( link, title, upload_by )
          else:
            return lang[1]
        open_url.close()
      except Exception as e:
        return "Error: {}".format( str( e ) )

  def search_images(lang, image, total: int = 3):
    try:
      lang       = config.database.take_lang_user( lang, "gis_answer" )
      save_total = int( total ) if str.isdigit( str( total ) ) else 3
      image  = urlparse.quote( image.replace( " ", "+" ) )
      url    = ("https://www.googleapis.com/customsearch/v1?q={}&num={}"
                "&safe=active&cx={}&key={}&searchType=image")
      url    = url.format( image, str(save_total), online_defs.apis["cx"], 
                          online_defs.apis["google_apis"] )
      with urlreq.urlopen( url ) as open_url:
        decode            = open_url.read().decode("utf-8")
        data              = json.loads( decode )
        total_imgs        = []
        if int( data["queries"]["request"][0]["totalResults"] ) is not 0:
          page_info       = data["items"]
          save_total_f    = save_total if len( page_info ) >= save_total else len( page_info )
          imgs            = [ page_info[x]["link"] for x in range( 0, save_total_f ) ]
          imgs_format     = [ ( total_imgs.append( "<b>%s)</b> %s" % ( x, c ) ) 
                                                                      ) for x, c in enumerate( imgs, start = 1 ) ]
          text            = lang[0].format( " ".join( total_imgs ) )
          return text
        else:
          return lang[1]
      open_url.close()
    except Exception as e:
      return "Error: {}".format( str( e ) )

#######
# End #
#######