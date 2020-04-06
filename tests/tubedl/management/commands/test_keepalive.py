import os
from unittest import mock

from tubedl.management.commands.keepalive import Command


def patch_requests_get():
    return mock.patch("tubedl.management.commands.keepalive.requests.get")


def patch_stdout_write():
    return mock.patch("django.core.management.base.OutputWrapper.write")


def patch_environ(environ=None):
    environ = environ or {}
    return mock.patch.dict(os.environ, environ, clear=True)


class TestCommand:
    def test_handle(self):
        environ = {}
        command = Command()
        with patch_environ(
            environ
        ), patch_stdout_write() as m_write, patch_requests_get() as m_get:
            command.handle()
        assert m_write.call_args_list == [
            mock.call("Couldn't keep alive, HOSTNAME not set")
        ]
        assert m_get.call_args_list == []
        environ = {"HOSTNAME": "tubedl.herokuapp.com"}
        with patch_environ(
            environ
        ), patch_stdout_write() as m_write, patch_requests_get() as m_get:
            command.handle()
        assert m_write.call_args_list == [mock.call('ping "tubedl.herokuapp.com"')]
        assert m_get.call_args_list == [mock.call("http://tubedl.herokuapp.com")]
