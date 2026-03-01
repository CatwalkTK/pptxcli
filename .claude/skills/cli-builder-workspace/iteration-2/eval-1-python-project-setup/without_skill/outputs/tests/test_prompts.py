"""Tests for the prompts module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from projinit.prompts import (
    prompt_confirm_creation,
    prompt_project_name,
    prompt_template_selection,
)


class TestPromptProjectName:
    """Tests for prompt_project_name."""

    @patch("projinit.prompts.questionary")
    def test_returns_entered_name(self, mock_q: MagicMock) -> None:
        """Test that the entered name is returned."""
        mock_q.text.return_value.ask.return_value = "my-project"
        result = prompt_project_name()
        assert result == "my-project"

    @patch("projinit.prompts.questionary")
    def test_strips_whitespace(self, mock_q: MagicMock) -> None:
        """Test that whitespace is trimmed from the name."""
        mock_q.text.return_value.ask.return_value = "  my-project  "
        result = prompt_project_name()
        assert result == "my-project"

    @patch("projinit.prompts.questionary")
    def test_raises_on_cancel(self, mock_q: MagicMock) -> None:
        """Test that KeyboardInterrupt is raised when user cancels."""
        mock_q.text.return_value.ask.return_value = None
        with pytest.raises(KeyboardInterrupt):
            prompt_project_name()

    @patch("projinit.prompts.questionary")
    def test_passes_default_value(self, mock_q: MagicMock) -> None:
        """Test that default value is passed to questionary."""
        mock_q.text.return_value.ask.return_value = "default-proj"
        prompt_project_name(default="default-proj")
        mock_q.text.assert_called_once()
        call_kwargs = mock_q.text.call_args
        assert call_kwargs.kwargs.get("default") == "default-proj" or call_kwargs[1].get("default") == "default-proj"


class TestPromptTemplateSelection:
    """Tests for prompt_template_selection."""

    @patch("projinit.prompts.questionary")
    def test_returns_selected_template(self, mock_q: MagicMock) -> None:
        """Test that the selected template name is returned."""
        mock_q.select.return_value.ask.return_value = "standard"
        mock_q.Choice = MagicMock(side_effect=lambda **kwargs: kwargs)
        result = prompt_template_selection()
        assert result == "standard"

    @patch("projinit.prompts.questionary")
    def test_raises_on_cancel(self, mock_q: MagicMock) -> None:
        """Test that KeyboardInterrupt is raised when user cancels."""
        mock_q.select.return_value.ask.return_value = None
        mock_q.Choice = MagicMock(side_effect=lambda **kwargs: kwargs)
        with pytest.raises(KeyboardInterrupt):
            prompt_template_selection()


class TestPromptConfirmCreation:
    """Tests for prompt_confirm_creation."""

    @patch("projinit.prompts.questionary")
    def test_returns_true_on_confirm(self, mock_q: MagicMock) -> None:
        """Test that True is returned when user confirms."""
        mock_q.confirm.return_value.ask.return_value = True
        assert prompt_confirm_creation("proj", "minimal") is True

    @patch("projinit.prompts.questionary")
    def test_returns_false_on_deny(self, mock_q: MagicMock) -> None:
        """Test that False is returned when user denies."""
        mock_q.confirm.return_value.ask.return_value = False
        assert prompt_confirm_creation("proj", "minimal") is False

    @patch("projinit.prompts.questionary")
    def test_returns_false_on_cancel(self, mock_q: MagicMock) -> None:
        """Test that False is returned when user cancels (None)."""
        mock_q.confirm.return_value.ask.return_value = None
        assert prompt_confirm_creation("proj", "minimal") is False
