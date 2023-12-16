import os
import pyttsx3
import pygame
import time
import pytest
from unittest.mock import Mock, MagicMock

# Import the module containing the function to be tested
from tts import playNdelete

# Mocking the necessary modules and functions
@pytest.fixture
def mock_modules(monkeypatch):
    mock_music = MagicMock(spec=pygame.mixer.music)
    monkeypatch.setattr(pyttsx3, 'init', Mock())
    monkeypatch.setattr(pygame.mixer, 'init', Mock())
    monkeypatch.setattr(pygame.mixer, 'music', mock_music)
    return mock_music

# Mocking 'os.remove'
@pytest.fixture
def mock_os_remove(monkeypatch):
    mock_remove = Mock()
    monkeypatch.setattr(os, 'remove', mock_remove)
    return mock_remove

# Test case
def test_playNdelete(mock_modules, mock_os_remove):
    # Mock the get_busy() function to return False after the first call
    mock_modules.get_busy.side_effect = [True, False]

    # Call the function and capture the return value
    result = playNdelete("Hello, this is a test.")
    
    # Assertions
    assert pyttsx3.init.called
    assert pygame.mixer.init.called

    assert pyttsx3.init().setProperty.called_with('rate', 120)
    assert pyttsx3.init().save_to_file.called_with("Hello, this is a test.", "saved_audio.wav")
    assert pyttsx3.init().runAndWait.called

    assert pygame.mixer.music.load.called_with("saved_audio.wav")
    assert pygame.mixer.music.play.called

    mock_os_remove.assert_called_once_with("saved_audio.wav")
    mock_os_remove().reset_mock()  # Reset mock calls for the next step

    # Check the return value
    assert result == "Audio played and deleted successfully."