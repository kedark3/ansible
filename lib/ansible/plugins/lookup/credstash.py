# (c) 2015, Ensighten <infra@ensighten.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

CREDSTASH_INSTALLED = False

try:
    import credstash
    CREDSTASH_INSTALLED = True
except ImportError:
    CREDSTASH_INSTALLED = False


if not CREDSTASH_INSTALLED:
    raise AnsibleError('The credstash lookup plugin requires credstash to be installed.')


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        if isinstance(terms, basestring):
            terms = [terms]

        ret = []
        for term in terms:
            try:
                val = credstash.getSecret(term, **kwargs)
            except credstash.ItemNotFound:
                raise AnsibleError('Key {} not found'.format(term))
            except Exception as e:
                raise AnsibleError('Encountered exception while fetching {}: {}'.format(term, e.message))
            ret.append(val)

        return ret
