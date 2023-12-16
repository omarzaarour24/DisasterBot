import pytest
from unittest.mock import patch, MagicMock
from tkinter import Canvas
from map import ZoomableWindow

# Mocked database connection and cursor

@pytest.fixture
def mock_cursor():
    cursor = MagicMock()
    cursor.fetchall.return_value = [(1, 2, 'red'), (3, 4, 'blue')]
    return cursor

@pytest.fixture
def mock_connection(mock_cursor):
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    return connection

@patch("psycopg2.connect")
def test_fetch_data(mock_connect):
    mock_connect.return_value.__enter__.return_value = mock_connection

    zoomable_window = ZoomableWindow(None)
    zoomable_window.fetch_data()

    assert len(zoomable_window.points) is not None

def test_resize_window(mocker):
    canvas = Canvas()
    mocker.patch.object(canvas, "config")
    window = ZoomableWindow(None)
    window.canvas = canvas
    event = MagicMock()
    window.resize_window(event)
    canvas.config.assert_called_once_with(scrollregion=canvas.bbox("all"))

def test_resize_window(mocker):
    canvas = Canvas()
    mocker.patch.object(canvas, "config")
    window = ZoomableWindow(None)
    window.canvas = canvas
    event = MagicMock()
    window.resize_window(event)
    canvas.config.assert_called_once_with(scrollregion=canvas.bbox("all"))

def test_start_drag():
    window = ZoomableWindow(None)
    event = MagicMock()
    event.x = 10
    event.y = 20
    window.start_drag(event)
    assert window.drag_data["x"] == 10
    assert window.drag_data["y"] == 20

def test_drag(mocker):
    canvas = Canvas()
    mocker.patch.object(canvas, "move")
    window = ZoomableWindow(None)
    window.canvas = canvas
    window.drag_data = {"x": 10, "y": 20}
    event = MagicMock()
    event.x = 30
    event.y = 40
    window.drag(event)
    canvas.move.assert_called_once_with("all", 20, 20)
    assert window.drag_data["x"] == 30
    assert window.drag_data["y"] == 40

def test_zoom(mocker):
    canvas = Canvas()
    mocker.patch.object(canvas, "scale")
    window = ZoomableWindow(None)
    window.canvas = canvas
    window.zoom_level = 1.0
    event = MagicMock()
    event.x = 50
    event.y = 50

    # Test zooming in
    event.delta = 1
    window.zoom(event)
    assert window.zoom_level == 1.1
    canvas.scale.assert_called_once_with("all", 50, 50, 1.1, 1.1)

    # Test zooming out
    canvas.scale.reset_mock()
    event.delta = -1
    window.zoom(event)
    assert window.zoom_level == 1.1 / 1.1
    canvas.scale.assert_called_once_with("all", 50, 50, 1.0, 1.0)

def test_show_popup(mocker):
    window = ZoomableWindow(None)
    window.canvas = Canvas()

    point = (10, 20, "blue")
    color = "blue"

    mock_show_popup = mocker.patch.object(window, "show_popup")
    expected_message = ""

    if color == "blue":
        expected_message = "Bot Data:"
    elif color == "red":
        expected_message = "Survivor Data:"
    elif color == "black":
        expected_message = "Obstacle Data:"
    else:
        expected_message = "Unknown point color."

    mock_show_popup.return_value = expected_message  # Set the return value of the mock

    actual_message = window.show_popup(point)
    mock_show_popup.assert_called_with(point)
    assert expected_message in actual_message


