import unittest.mock

import pytest

import nested_diff_restful


def test_wsgi_server_entry_point(capsys):
    with unittest.mock.patch('sys.argv', ['nested_diff_restful', '--help']):
        with pytest.raises(SystemExit) as e:
            nested_diff_restful.start_wsgi_server()

        assert e.value.code == 0

    captured = capsys.readouterr()

    assert captured.out.startswith('usage: nested_diff_restful')
    assert captured.err == ''


def test_wsgi_server_version(capsys):
    with unittest.mock.patch('sys.argv', ['nested_diff_restful', '--version']):
        with pytest.raises(SystemExit) as e:
            nested_diff_restful.start_wsgi_server()

        assert e.value.code == 0

    captured = capsys.readouterr()

    assert (
        captured.out
        == f'nested_diff_restful (version {nested_diff_restful.__version__})\n'
    )
    assert captured.err == ''
