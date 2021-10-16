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

from unittest import mock

from openstack.shared_file_system.v2 import _proxy
from openstack.shared_file_system.v2 import limit
from openstack.shared_file_system.v2 import share
from openstack.shared_file_system.v2 import share_instance
from openstack.shared_file_system.v2 import share_network
from openstack.shared_file_system.v2 import share_snapshot
from openstack.shared_file_system.v2 import share_snapshot_instance
from openstack.shared_file_system.v2 import storage_pool
from openstack.shared_file_system.v2 import user_message
from openstack.tests.unit import test_proxy_base


class TestSharedFileSystemProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestSharedFileSystemProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSharedFileSystemShare(TestSharedFileSystemProxy):
    def test_shares(self):
        self.verify_list(self.proxy.shares, share.Share)

    def test_shares_detailed(self):
        self.verify_list(self.proxy.shares, share.Share,
                         method_kwargs={"details": True, "query": 1},
                         expected_kwargs={"query": 1})

    def test_shares_not_detailed(self):
        self.verify_list(self.proxy.shares, share.Share,
                         method_kwargs={"details": False, "query": 1},
                         expected_kwargs={"query": 1})

    def test_share_get(self):
        self.verify_get(self.proxy.get_share, share.Share)

    def test_share_delete(self):
        self.verify_delete(
            self.proxy.delete_share, share.Share, False)

    def test_share_delete_ignore(self):
        self.verify_delete(
            self.proxy.delete_share, share.Share, True)

    def test_share_create(self):
        self.verify_create(self.proxy.create_share, share.Share)

    def test_share_update(self):
        self.verify_update(self.proxy.update_share, share.Share)

    def test_share_instances(self):
        self.verify_list(self.proxy.share_instances,
                         share_instance.ShareInstance)

    def test_share_instance_get(self):
        self.verify_get(self.proxy.get_share_instance,
                        share_instance.ShareInstance)

    def test_share_instance_reset(self):
        self._verify(
            "openstack.shared_file_system.v2.share_instance."
            + "ShareInstance.reset_status",
            self.proxy.reset_share_instance_status,
            method_args=['id', 'available'],
            expected_args=[self.proxy, 'available'],
        )

    def test_share_instance_delete(self):
        self._verify(
            "openstack.shared_file_system.v2.share_instance."
            + "ShareInstance.force_delete",
            self.proxy.delete_share_instance,
            method_args=['id'],
            expected_args=[self.proxy])

    @mock.patch("openstack.resource.wait_for_status")
    def test_wait_for(self, mock_wait):
        mock_resource = mock.Mock()
        mock_wait.return_value = mock_resource

        self.proxy.wait_for_status(mock_resource, 'ACTIVE')

        mock_wait.assert_called_once_with(self.proxy, mock_resource,
                                          'ACTIVE', [], 2, 120)


class TestSharedFileSystemStoragePool(TestSharedFileSystemProxy):
    def test_storage_pools(self):
        self.verify_list(
            self.proxy.storage_pools, storage_pool.StoragePool)

    def test_storage_pool_detailed(self):
        self.verify_list(
            self.proxy.storage_pools, storage_pool.StoragePool,
            method_kwargs={"details": True, "backend": "alpha"},
            expected_kwargs={"backend": "alpha"})

    def test_storage_pool_not_detailed(self):
        self.verify_list(
            self.proxy.storage_pools, storage_pool.StoragePool,
            method_kwargs={"details": False, "backend": "alpha"},
            expected_kwargs={"backend": "alpha"})


class TestUserMessageProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestUserMessageProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_user_messages(self):
        self.verify_list(self.proxy.user_messages, user_message.UserMessage)

    def test_user_messages_queried(self):
        self.verify_list(
            self.proxy.user_messages, user_message.UserMessage,
            method_kwargs={"action_id": "1"},
            expected_kwargs={"action_id": "1"})

    def test_user_message_get(self):
        self.verify_get(self.proxy.get_user_message, user_message.UserMessage)

    def test_delete_user_message(self):
        self.verify_delete(
            self.proxy.delete_user_message, user_message.UserMessage, False)

    def test_delete_user_message_true(self):
        self.verify_delete(
            self.proxy.delete_user_message, user_message.UserMessage, True)

    def test_limit(self):
        self.verify_list(self.proxy.limits, limit.Limit)


class TestShareSnapshotResource(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestShareSnapshotResource, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_share_snapshots(self):
        self.verify_list(
            self.proxy.share_snapshots, share_snapshot.ShareSnapshot)

    def test_share_snapshots_detailed(self):
        self.verify_list(
            self.proxy.share_snapshots,
            share_snapshot.ShareSnapshot,
            method_kwargs={"details": True, "name": "my_snapshot"},
            expected_kwargs={"name": "my_snapshot"})

    def test_share_snapshots_not_detailed(self):
        self.verify_list(
            self.proxy.share_snapshots,
            share_snapshot.ShareSnapshot,
            method_kwargs={"details": False, "name": "my_snapshot"},
            expected_kwargs={"name": "my_snapshot"})

    def test_share_snapshot_get(self):
        self.verify_get(
            self.proxy.get_share_snapshot, share_snapshot.ShareSnapshot)

    def test_share_snapshot_delete(self):
        self.verify_delete(
            self.proxy.delete_share_snapshot,
            share_snapshot.ShareSnapshot, False)

    def test_share_snapshot_delete_ignore(self):
        self.verify_delete(
            self.proxy.delete_share_snapshot,
            share_snapshot.ShareSnapshot, True)

    def test_share_snapshot_create(self):
        self.verify_create(
            self.proxy.create_share_snapshot, share_snapshot.ShareSnapshot)

    def test_share_snapshot_update(self):
        self.verify_update(
            self.proxy.update_share_snapshot, share_snapshot.ShareSnapshot)

    @mock.patch("openstack.resource.wait_for_delete")
    def test_wait_for_delete(self, mock_wait):
        mock_resource = mock.Mock()
        mock_wait.return_value = mock_resource

        self.proxy.wait_for_delete(mock_resource)

        mock_wait.assert_called_once_with(self.proxy, mock_resource, 2, 120)


class TestShareSnapshotInstanceResource(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestShareSnapshotInstanceResource, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_share_snapshot_instances(self):
        self.verify_list(
            self.proxy.share_snapshot_instances,
            share_snapshot_instance.ShareSnapshotInstance)

    def test_share_snapshot_instance_detailed(self):
        self.verify_list(self.proxy.share_snapshot_instances,
                         share_snapshot_instance.ShareSnapshotInstance,
                         method_kwargs={
                             "details": True,
                             "query": {'snapshot_id': 'fake'}
                         },
                         expected_kwargs={"query": {'snapshot_id': 'fake'}})

    def test_share_snapshot_instance_not_detailed(self):
        self.verify_list(self.proxy.share_snapshot_instances,
                         share_snapshot_instance.ShareSnapshotInstance,
                         method_kwargs={
                             "details": False,
                             "query": {'snapshot_id': 'fake'}
                         },
                         expected_kwargs={"query": {'snapshot_id': 'fake'}})

    def test_share_snapshot_instance_get(self):
        self.verify_get(
            self.proxy.get_share_snapshot_instance,
            share_snapshot_instance.ShareSnapshotInstance)


class TestShareNetworkResource(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestShareNetworkResource, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_share_networks(self):
        self.verify_list(self.proxy.share_networks, share_network.ShareNetwork)

    def test_share_networks_detailed(self):
        self.verify_list(self.proxy.share_networks, share_network.ShareNetwork,
                         method_kwargs={"details": True, "name": "my_net"},
                         expected_kwargs={"name": "my_net"})

    def test_share_networks_not_detailed(self):
        self.verify_list(self.proxy.share_networks, share_network.ShareNetwork,
                         method_kwargs={"details": False, "name": "my_net"},
                         expected_kwargs={"name": "my_net"})

    def test_share_network_get(self):
        self.verify_get(
            self.proxy.get_share_network, share_network.ShareNetwork)

    def test_share_network_delete(self):
        self.verify_delete(
            self.proxy.delete_share_network, share_network.ShareNetwork, False)

    def test_share_network_delete_ignore(self):
        self.verify_delete(
            self.proxy.delete_share_network, share_network.ShareNetwork, True)

    def test_share_network_create(self):
        self.verify_create(
            self.proxy.create_share_network, share_network.ShareNetwork)

    def test_share_network_update(self):
        self.verify_update(
            self.proxy.update_share_network, share_network.ShareNetwork)
