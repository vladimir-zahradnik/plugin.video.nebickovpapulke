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
    _host = 'www.nebickovpapulke.sk:80'
    _user_agent = 'Mozilla/6.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.5) Gecko/2008092417 Firefox/3.0.3'

    def __init__(self, items_per_page=50):
        HttpClient.__init__(self, default_header={'Accept-Encoding': 'gzip',
                                                  'Host': self._host,
                                                  'Connection': 'Keep-Alive',
                                                  'User-Agent': self._user_agent})
        self._items_per_page = items_per_page

    def _create_url(self, path):
        return 'http://{0}/{1}'.format(unicode(self._host, 'utf-8'), unicode(path, 'utf-8'))
