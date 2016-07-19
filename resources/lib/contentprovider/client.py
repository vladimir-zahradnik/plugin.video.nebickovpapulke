# -*- coding: UTF-8 -*-
# /*
# *      Copyright (C) 2016 Vladimir Zahradnik
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

__author__ = 'vladimir.zahradnik'

from resources.lib.http import HttpClient

class Client(HttpClient):

    def __init__(self, access_token='', client_id='', client_secret='', items_per_page=50):
        HttpClient.__init__(self, default_header={'Accept-Encoding': 'gzip',
                                                               'Host': 'api.soundcloud.com:443',
                                                               'Connection': 'Keep-Alive',
                                                               'User-Agent': 'SoundCloud-Android/15.09.14-release (Android 5.0.1; samsung GT-I9505)'})
        self._access_token = access_token
        self._items_per_page = items_per_page

        # set client id with fallback
        self._client_id = self.CLIENT_ID
        if client_id:
            self._client_id = client_id
            pass

        # set client secret with fallback
        self._client_secret = self.CLIENT_SECRET
        if client_secret:
            self._client_secret = client_secret
            pass
        pass
