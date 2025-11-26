"""Tests for SupportAgentTools."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from agent.knowledge.wiki_source import WikiKnowledgeSource
from agent.tools import SupportAgentTools


@pytest.fixture
def mock_wiki_source():
    """Create a mock WikiKnowledgeSource."""
    mock = Mock(spec=WikiKnowledgeSource)
    return mock


@pytest.fixture
def tools(mock_wiki_source):
    """Create SupportAgentTools with mock wiki source."""
    return SupportAgentTools(mock_wiki_source)


class TestSearchWiki:
    """Tests for search_wiki tool."""

    def test_search_finds_matching_content(self, tools, mock_wiki_source):
        """Test that search returns content when keywords match."""
        mock_wiki_source.list_files.return_value = [Path("doc1.md"), Path("doc2.md")]
        mock_wiki_source.load_file.side_effect = [
            "This document contains Lambda information",
            "This document is about S3 buckets",
        ]

        result = tools.search_wiki("lambda")

        mock_wiki_source.clone_or_update.assert_called_once()
        assert "Lambda information" in result
        assert "## From doc1.md" in result

    def test_search_returns_no_results_message(self, tools, mock_wiki_source):
        """Test that search returns appropriate message when no matches found."""
        mock_wiki_source.list_files.return_value = [Path("doc1.md")]
        mock_wiki_source.load_file.return_value = "Content about S3"

        result = tools.search_wiki("lambda")

        assert "No relevant content found for query: lambda" in result

    def test_search_handles_multiple_keywords(self, tools, mock_wiki_source):
        """Test that search matches any keyword in query."""
        mock_wiki_source.list_files.return_value = [Path("doc1.md")]
        mock_wiki_source.load_file.return_value = "Lambda functions are great"

        result = tools.search_wiki("lambda ec2")

        assert "Lambda functions" in result

    def test_search_is_case_insensitive(self, tools, mock_wiki_source):
        """Test that search is case insensitive."""
        mock_wiki_source.list_files.return_value = [Path("doc1.md")]
        mock_wiki_source.load_file.return_value = "AWS Lambda Functions"

        result = tools.search_wiki("lambda")

        assert "Lambda Functions" in result

    def test_search_handles_error(self, tools, mock_wiki_source):
        """Test that search returns error message when operation fails."""
        mock_wiki_source.clone_or_update.side_effect = Exception("Clone failed")

        result = tools.search_wiki("lambda")

        assert "Error searching wiki: Clone failed" in result


class TestListWikiFiles:
    """Tests for list_wiki_files tool."""

    def test_list_returns_available_files(self, tools, mock_wiki_source):
        """Test that list returns all available files."""
        mock_wiki_source.list_files.return_value = [
            Path("doc1.md"),
            Path("doc2.md"),
            Path("image.png"),
        ]

        result = tools.list_wiki_files()

        assert "doc1.md" in result
        assert "doc2.md" in result
        assert "image.png" in result

    def test_list_calls_clone_or_update(self, tools, mock_wiki_source):
        """Test that list updates repository before listing."""
        mock_wiki_source.list_files.return_value = []

        tools.list_wiki_files()

        mock_wiki_source.clone_or_update.assert_called_once()

    def test_list_handles_error(self, tools, mock_wiki_source):
        """Test that list returns error message on failure."""
        mock_wiki_source.clone_or_update.side_effect = Exception("Update failed")

        result = tools.list_wiki_files()

        assert "Error listing wiki files: Update failed" in result
