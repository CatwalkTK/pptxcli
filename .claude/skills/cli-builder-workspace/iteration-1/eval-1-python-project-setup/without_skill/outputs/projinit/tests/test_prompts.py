"""Tests for the prompts module (validation logic only -- no interactive tests)."""

from projinit.prompts import _validate_project_name


class TestValidateProjectName:
    """Tests for project name validation."""

    def test_valid_simple_name(self):
        assert _validate_project_name("myproject") is True

    def test_valid_with_hyphens(self):
        assert _validate_project_name("my-project") is True

    def test_valid_with_underscores(self):
        assert _validate_project_name("my_project") is True

    def test_valid_with_digits(self):
        assert _validate_project_name("project123") is True

    def test_valid_single_letter(self):
        assert _validate_project_name("a") is True

    def test_empty_string_rejected(self):
        result = _validate_project_name("")
        assert isinstance(result, str)
        assert "empty" in result.lower()

    def test_whitespace_only_rejected(self):
        result = _validate_project_name("   ")
        assert isinstance(result, str)

    def test_starts_with_digit_rejected(self):
        result = _validate_project_name("123project")
        assert isinstance(result, str)

    def test_starts_with_hyphen_rejected(self):
        result = _validate_project_name("-project")
        assert isinstance(result, str)

    def test_special_characters_rejected(self):
        result = _validate_project_name("my@project")
        assert isinstance(result, str)

    def test_spaces_in_name_rejected(self):
        result = _validate_project_name("my project")
        assert isinstance(result, str)

    def test_max_length_accepted(self):
        name = "a" * 64
        assert _validate_project_name(name) is True

    def test_over_max_length_rejected(self):
        name = "a" * 65
        result = _validate_project_name(name)
        assert isinstance(result, str)
