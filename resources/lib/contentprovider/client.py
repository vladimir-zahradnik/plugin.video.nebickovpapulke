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
from resources.lib.exceptions.ProviderException import ProviderException
from resources.lib.http import HttpClient

__author__ = 'vladimir.zahradnik'


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
        return 'http://{0}/{1}'.format(unicode(self._host, 'utf-8'), unicode(path.strip('/'), 'utf-8'))

    @staticmethod
    def _create_params(page=1):
        params = {}
        if page > 1:
            params['page'] = str(page - 1)

        return params

    @staticmethod
    def _handle_error(response):
        status_class = response.status_code / 100
        # accept 2XX and 3XX
        if status_class != 2 and status_class != 3 and status_class != 5:
            json_data = response.json()
            error_message = 'HTTP error %d' % response.status_code
            if 'error' in json_data:
                error_message = json_data['error']
                pass

            if 'errors' in json_data:
                errors = json_data['errors']
                if len(errors) > 0:
                    error_message = errors[0].get('error_message', '')
                pass

            # last fallback
            if not error_message:
                error_message = response.headers.get('status', error_message)
                pass
            raise ProviderException(error_message)
        pass

    def get_episodes(self, page=1):
        params = self._create_params(page)
        response = self._request(self._create_url('epizody'),
                                 headers={'Accept': 'text/html'},
                                 params=params)
        self._handle_error(response)
        # return items.convert_to_items(response.json())
        return response
