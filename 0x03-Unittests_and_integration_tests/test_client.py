#!/usr/bin/env python3
"""
Unit tests for client.py
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for client.GithubOrgClient
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, test_payload)

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL."""
        known_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, known_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repos."""
        json_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = json_payload

        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            public_repos_url = "https://api.github.com/orgs/google/repos"
            mock_public_repos_url.return_value = public_repos_url
            client = GithubOrgClient("google")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(public_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for the GithubOrgClient class."""

    @classmethod
    def setUpClass(cls):
        """Set up class for integration tests."""
        route_payload = {
            cls.org_payload["repos_url"]: cls.repos_payload,
        }

        def side_effect(url):
            """Side effect for requests.get mock."""
            mock_response = Mock()
            if url in route_payload:
                mock_response.json.return_value = route_payload[url]
                return mock_response
            mock_response.json.return_value = cls.org_payload
            return mock_response

        cls.get_patcher = patch('utils.requests.get', side_effect=side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class for integration tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license."""
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
