import json
import uuid
from unittest.mock import patch

from django.test import TestCase

from authentication.factories import UserFactory, set_up_authentication
from strategy.factories import (
    StrategyFactory,
    StrategySharingFactory,
    UserStrategyFactory,
)

TEST_UUIDS_COUNT = 0


def mock_uuid():
    global TEST_UUIDS_COUNT
    TEST_UUIDS_COUNT += 1
    return uuid.UUID(int=TEST_UUIDS_COUNT)


def fixed_mock_uuid():
    return uuid.UUID(int=0)


def mock_now():
    return "2012-11-01T04:16:13-04:00"


class DeleteStrategyViewTest(TestCase):
    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_ok(self):
        auth = set_up_authentication()

        UserStrategyFactory(user=auth["user"], strategy=uuid.uuid4())

        response = self.client.post(
            f"/strategy/deleteStrategy/{uuid.uuid4()}",
            {},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"status": "true"})

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_strategy_delete_with_commits(self):
        auth = set_up_authentication()

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=uuid.uuid4())

        StrategyFactory(
            strategy=user_strategy,
            commit=uuid.uuid4(),
            flow_metadata={},
            input={},
            output={},
        )

        response = self.client.post(
            f"/strategy/deleteStrategy/{uuid.uuid4()}",
            {},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"status": "true"})

    def test_strategy_id_dne(self):
        auth = set_up_authentication()

        response = self.client.post(
            f"/strategy/deleteStrategy/{uuid.uuid4()}",
            {},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.json(), {"error": "Strategy ID does not exist"})

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_different_user_tries_to_delete_strategy(self):
        auth_1 = set_up_authentication()
        auth_2 = set_up_authentication()

        UserStrategyFactory(user=auth_1["user"], strategy=uuid.uuid4())

        response = self.client.post(
            f"/strategy/deleteStrategy/{uuid.uuid4()}",
            {},
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth_2['token']}"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(response.json(), {"error": "Strategy ID does not exist"})


class StrategyViewTest(TestCase):
    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_ok(self):
        auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id = "28061176-a818-4525-a238-c9a73c6418f1"

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={},
            output={},
        )

        response = self.client.get(
            f"/strategy/{strategy_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"elements": {}, "inputs": {}, "outputs": {}}
        )

    def test_strategy_id_dne(self):
        auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"

        response = self.client.get(
            f"/strategy/{strategy_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        assert response.status_code == 401
        self.assertDictEqual(
            response.json(), {"error": "You are not authorized to view this strategy"}
        )

    def test_strategy_id_does_not_belong_to_user_and_is_not_shared(self):
        auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id = "28061176-a818-4525-a238-c9a73c6418f1"

        user = UserFactory()
        user_strategy = UserStrategyFactory(user=user, strategy=strategy_id)

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={},
            output={},
        )

        response = self.client.get(
            f"/strategy/{strategy_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        assert response.status_code == 401
        self.assertDictEqual(
            response.json(), {"error": "You are not authorized to view this strategy"}
        )

    def test_shared_user_can_view_strategy(self):
        auth = set_up_authentication()
        shared_auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id = "28061176-a818-4525-a238-c9a73c6418f1"

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=strategy_id)
        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={},
            output={},
        )

        StrategySharingFactory(
            strategy=user_strategy, user=shared_auth["user"], permissions=2
        )

        response = self.client.get(
            f"/strategy/{strategy_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"elements": {}, "inputs": {}, "outputs": {}}
        )


class CommitIdViewTest(TestCase):
    @patch("uuid.uuid4", mock_uuid)
    def test_ok(self):
        auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"

        UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        response = self.client.get(
            f"/strategy/{strategy_id}/commitId",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "strategyId": "5f4a0050-6766-40e1-946c-ddbd5533a3d1",
                "commitId": "00000000-0000-0000-0000-000000000001",
            },
        )

    def test_strategy_id_dne(self):
        auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"

        response = self.client.get(
            f"/strategy/{strategy_id}/commitId",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "Strategy does not exist"})

    @patch("uuid.uuid4", fixed_mock_uuid)
    def test_shared_user_returns_ok(self):
        auth = set_up_authentication()
        sharing_auth = set_up_authentication()

        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=strategy_id)
        StrategySharingFactory(
            strategy=user_strategy, user=sharing_auth["user"], permissions=2
        )

        response = self.client.get(
            f"/strategy/{strategy_id}/commitId",
            **{"HTTP_AUTHORIZATION": f"Bearer {sharing_auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {
                "strategyId": "5f4a0050-6766-40e1-946c-ddbd5533a3d1",
                "commitId": "00000000-0000-0000-0000-000000000000",
            },
        )

    def test_non_shared_user_returns_error(self):
        auth = set_up_authentication()
        sharing_auth = set_up_authentication()

        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"

        UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        response = self.client.get(
            f"/strategy/{strategy_id}/commitId",
            **{"HTTP_AUTHORIZATION": f"Bearer {sharing_auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {"error": "Strategy does not exist"},
        )


class StrategyCommitGetViewTest(TestCase):
    def test_ok(self):
        auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id_one = "28061176-a818-4525-a238-c9a73c6418f1"
        commit_id_two = "690d738c-bbd1-463f-99d2-00c8ebad6d30"

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id_one,
            flow_metadata={},
            input={"1": {}},
            output={"1": {}},
        )

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id_two,
            flow_metadata={},
            input={"1": {}, "2": {}},
            output={"1": {}, "2": {}},
        )

        response_one = self.client.get(
            f"/strategy/{strategy_id}/{commit_id_one}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        response_two = self.client.get(
            f"/strategy/{strategy_id}/{commit_id_two}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response_one.json(),
            {"elements": {}, "inputs": {"1": {}}, "outputs": {"1": {}}},
        )

        self.assertDictEqual(
            response_two.json(),
            {
                "elements": {},
                "inputs": {"1": {}, "2": {}},
                "outputs": {"1": {}, "2": {}},
            },
        )

    def test_commit_id_dne(self):
        auth = set_up_authentication()
        strategy_id = "5f4a0050-6766-40e1-946c-ddbd5533a3d1"
        commit_id = "26fed45a-20f3-47b0-819c-c17bfe22774a"

        UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        response = self.client.get(
            f"/strategy/{strategy_id}/{commit_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "ID does not exist"})

    def test_strategy_id_dne(self):
        auth = set_up_authentication()
        strategy_id = "093aa9d0-36ca-4479-a0fb-391b68c8c053"
        commit_id = "45ee011d-d90e-4edd-8698-45955925edbb"

        response = self.client.get(
            f"/strategy/{strategy_id}/{commit_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"error": "You are not authorized to view this strategy"}
        )

    def test_strategy_id_invalid(self):
        auth = set_up_authentication()
        strategy_id = "strategy_id_invalid"
        commit_id = "commit_id_invalid"

        response = self.client.get(
            f"/strategy/{strategy_id}/{commit_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"validation_error": "There was a validation error"}
        )

    def test_commit_id_invalid(self):
        auth = set_up_authentication()
        strategy_id = "093aa9d0-36ca-4479-a0fb-391b68c8c053"
        commit_id = "commit_id_invalid"

        UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        response = self.client.get(
            f"/strategy/{strategy_id}/{commit_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"validation_error": "There was a validation error"}
        )

    def test_user_not_associated_with_strategy(self):
        auth = set_up_authentication()
        strategy_id = "093aa9d0-36ca-4479-a0fb-391b68c8c053"
        commit_id = "45ee011d-d90e-4edd-8698-45955925edbb"

        user = UserFactory()
        user_strategy = UserStrategyFactory(user=user, strategy=strategy_id)

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={},
            output={},
        )

        response = self.client.get(
            f"/strategy/{strategy_id}/{commit_id}",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"error": "You are not authorized to view this strategy"}
        )


class StrategyCommitPostViewTest(TestCase):
    def test_ok(self):
        auth = set_up_authentication()
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        payload = {"metadata": {}, "inputs": {}, "outputs": {}}

        response = self.client.post(
            f"/strategy/{strategy_id}/{commit_id}",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"message": "Successfully saved strategy "}
        )

    def test_strategy_id_doesnt_exist(self):
        auth = set_up_authentication()
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        payload = {
            "strategy_name": "Test Strategy",
            "metadata": {},
            "inputs": {},
            "outputs": {},
        }

        response = self.client.post(
            f"/strategy/{strategy_id}/{commit_id}",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "This strategy does not exist"})

    def test_strategy_commit_already_exists(self):
        auth = set_up_authentication()
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=strategy_id)

        StrategyFactory(
            strategy=user_strategy,
            commit=commit_id,
            flow_metadata={},
            input={"1": {}},
            output={"1": {}},
        )

        payload = {"metadata": {}, "inputs": {}, "outputs": {}}

        response = self.client.post(
            f"/strategy/{strategy_id}/{commit_id}",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"error": "The strategy-commit pair already exist"}
        )

    def test_strategy_id_not_valid(self):
        auth = set_up_authentication()
        strategy_id = "strategy_id_invalid"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        payload = {"metadata": {}, "inputs": {}, "outputs": {}}

        response = self.client.post(
            f"/strategy/{strategy_id}/{commit_id}",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "There was a validation error"})

    def test_commit_id_not_valid(self):
        auth = set_up_authentication()
        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "commit_id_invalid"

        payload = {
            "strategy_name": "Test Strategy",
            "metadata": {},
            "inputs": {},
            "outputs": {},
        }

        response = self.client.post(
            f"/strategy/{strategy_id}/{commit_id}",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {auth['token']}"},
        )

        self.assertDictEqual(response.json(), {"error": "This strategy does not exist"})

    def test_shared_user_with_write_permissions_can_save(self):
        auth = set_up_authentication()
        shared_auth = set_up_authentication()

        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=strategy_id)
        StrategySharingFactory(
            strategy=user_strategy, user=shared_auth["user"], permissions=2
        )

        payload = {
            "strategy_name": "Test Strategy",
            "metadata": {},
            "inputs": {},
            "outputs": {},
        }

        response = self.client.post(
            f"/strategy/{strategy_id}/{commit_id}",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {shared_auth['token']}"},
        )

        self.assertDictEqual(
            response.json(), {"message": "Successfully saved strategy "}
        )

    def test_shared_user_with_read_permissions_cannot_save(self):
        auth = set_up_authentication()
        shared_auth = set_up_authentication()

        strategy_id = "136f0d6e-1e32-4edb-ac5e-1676047425d2"
        commit_id = "c98d7e19-673b-4609-9b32-6f827fe515e6"

        user_strategy = UserStrategyFactory(user=auth["user"], strategy=strategy_id)
        StrategySharingFactory(
            strategy=user_strategy, user=shared_auth["user"], permissions=1
        )

        payload = {
            "strategy_name": "Test Strategy",
            "metadata": {},
            "inputs": {},
            "outputs": {},
        }

        response = self.client.post(
            f"/strategy/{strategy_id}/{commit_id}",
            json.dumps(payload),
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Bearer {shared_auth['token']}"},
        )

        self.assertDictEqual(
            response.json(),
            {"error": "You only have read permissions on this strategy"},
        )
