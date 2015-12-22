# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools

from openstack.cluster.v1 import receiver


FAKE_ID = 'ae63a10b-4a90-452c-aef1-113a0b255ee3'
FAKE_NAME = 'test_receiver'

FAKE = {
    'name': FAKE_NAME,
    'type': 'webhook',
    'cluster_id': 'FAKE_CLUSTER',
    'action': 'CLUSTER_RESIZE',
    'created_time': '2015-08-10T09:14:53',
    'deleted_time': None,
    'actor': {},
    'params': {
        'adjustment_type': 'CHANGE_IN_CAPACITY',
        'adjustment': 2
    },
    'channel': {
        'alarm_url': 'http://host:port/webhooks/AN_ID/trigger?V=1',
    },
    'user': 'FAKE_USER',
    'project': 'FAKE_PROJECT',
    'domain': '',
}


class TestReceiver(testtools.TestCase):

    def setUp(self):
        super(TestReceiver, self).setUp()

    def test_basic(self):
        sot = receiver.Receiver()
        self.assertEqual('receiver', sot.resource_key)
        self.assertEqual('receivers', sot.resources_key)
        self.assertEqual('/receivers', sot.base_path)
        self.assertEqual('clustering', sot.service.service_type)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_retrieve)
        self.assertFalse(sot.allow_update)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)

    def test_instantiate(self):
        sot = receiver.Receiver(FAKE)
        self.assertIsNone(sot.id)
        self.assertEqual(FAKE['name'], sot.name)
        self.assertEqual(FAKE['type'], sot.type)
        self.assertEqual(FAKE['cluster_id'], sot.cluster.id)
        self.assertEqual(FAKE['action'], sot.action)
        self.assertEqual(FAKE['params'], sot.params)
        self.assertEqual(FAKE['created_time'], sot.created_at)
        self.assertEqual(FAKE['deleted_time'], sot.deleted_at)
        self.assertEqual(FAKE['user'], sot.user)
        self.assertEqual(FAKE['project'], sot.project)
        self.assertEqual(FAKE['domain'], sot.domain)
        self.assertEqual(FAKE['channel'], sot.channel)
