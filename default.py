# -*- coding: UTF-8 -*-
# *
# *      Copyright (C) 2015 Vladimir Zahradnik
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import sys
import re
import xbmc, xbmcplugin, xbmcgui, xbmcaddon
import urllib, urllib2, urlparse

web_base_url = 'http://www.nebickovpapulke.sk'
addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

MODE_LIST_EPISODES = 'list_episodes'
MODE_VIEW_EPISODE_DETAILS = 'episode_details'
MODE_PLAY_EPISODE = 'play_episode'

def build_url(query):
    addon_base_url = sys.argv[0]

    # Remove query items which have meaningless value
    query = {k: v for k, v in query.iteritems() if v}

    return addon_base_url + '?' + urllib.urlencode(query)

def get_http_data_from_url(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0'
    request = urllib2.Request(url)
    request.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(request)
    httpdata = response.read()
    response.close()
    return httpdata

def notify(msg, timeout = 5000):
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addon.getAddonInfo('name'), msg,
                                                        timeout, addon.getAddonInfo('icon')))

def add_item(name, mode, url=None, plugin_url=None, isFolder=False):

    if not plugin_url:
        plugin_url = build_url({'url': url, 'mode': mode, 'name': name})

    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png")

    notify(plugin_url)
    result = xbmcplugin.addDirectoryItem(handle=addon_handle, url=plugin_url,
                                         listitem=li, isFolder=isFolder)
    return result


def add_directory(name, mode, url):
    return add_item(name, mode, url, isFolder=True)


def translate(id):
    return addon.getLocalizedString(id).encode('utf-8')

def list_archived_shows():
    url = args.get('url', None)

    if url is None:
        url = web_base_url + '/epizody'
    else:
        url = url[0]

    content = get_http_data_from_url(url)

    # Limit result to only Epizode Archive part
    content = content[content.find('Archív Epizód') : content.find('<aside class="second">')]

    # Regexp to match aired date and epizode name
    pattern = 'class="date-display-single">(\d{2}.\d{2}.\d{4})<\/span>.*?<a href="(.*?)">Epizóda (\d{2}\/\d{4})\s*:*\s*(.*?)<\/a>'
    match = re.compile(pattern, re.DOTALL).findall(content)

    for aired, url, episode, name in match:
        add_directory(translate(30000) + " " + episode + ": " + name, MODE_VIEW_EPISODE_DETAILS, web_base_url + url)

    # Check if there is more episodes
    pattern = 'class="pager-next.*?<a href="(.*?)"'
    match = re.compile(pattern, re.DOTALL).findall(content)

    if match:
        url = match[0]
        add_directory("[B]" + translate(30001) +"[/B]", MODE_LIST_EPISODES, web_base_url + url)

    xbmcplugin.endOfDirectory(addon_handle)

def view_episode_details():
    url = args.get('url')[0]

    content = get_http_data_from_url(url)

    # Parse episode info and get Video ID for Vimeo
    pattern = 'player.vimeo.com/video/(\d+)\?'
    match = re.compile(pattern).findall(content)

    if match:
        add_item('Epizoda', MODE_PLAY_EPISODE, plugin_url='plugin://plugin.video.vimeo/play/?video_id=' + match[0])

    notify('plugin://plugin.video.vimeo/play/?video_id=' + match[0])
    xbmcplugin.endOfDirectory(addon_handle)


mode = args.get('mode', None)

if mode is None or mode[0] == MODE_LIST_EPISODES:
    list_archived_shows()

elif mode[0] == MODE_VIEW_EPISODE_DETAILS:
    view_episode_details()
