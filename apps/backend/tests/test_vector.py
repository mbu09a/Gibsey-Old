import pytest
from unittest.mock import patch, MagicMock


class DummyEmbed:
    def __init__(self):
        # Deterministic small vectors for testing
        self.vectors = {
            "q1": [0.9, 0.1],
            "q2": [0.1, 0.9],
            "mixed": [0.5, 0.5]
        }
        
    def create(self, **kwargs):
        query = kwargs.get("input", "q1")
        # For testing purposes, treat the input as a key to our predefined vectors
        vector = self.vectors.get(query, self.vectors["q1"])
        
        class Response:
            class EmbeddingData:
                def __init__(self, vec):
                    self.embedding = vec
            
            data = [EmbeddingData(vector)]
        
        return Response()


def test_embed():
    """Test the _embed function with a mock OpenAI client."""
    with patch("app.vector.client", DummyEmbed()):
        from app.vector import _embed
        
        # Test with a known query
        result = _embed("q1")
        assert result == [0.9, 0.1]
        
        # Test with a different query
        result = _embed("q2")
        assert result == [0.1, 0.9]


def test_similar_pages():
    """Test the similar_pages function with mocked dependencies."""
    # Mock both OpenAI client and Supabase client
    with patch("app.vector.client", DummyEmbed()):
        from app.vector import similar_pages
        
        # Create mock for Supabase RPC result
        mock_db_result = MagicMock()
        mock_db_result.execute.return_value.data = [
            {"id": 1, "title": "Page 1", "content": "Content 1", "score": 0.95},
            {"id": 2, "title": "Page 2", "content": "Content 2", "score": 0.85},
            {"id": 3, "title": "Page 3", "content": "Content 3", "score": 0.75}
        ]
        
        # Mock the Supabase client
        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value = mock_db_result
        
        # Patch the Supabase.client() method
        with patch("app.vector.Supabase.client", return_value=mock_supabase):
            # Test with k=3
            results = similar_pages("test query", k=3)
            
            # Check that the correct number of results is returned
            assert len(results) == 3
            
            # Check that the results have the expected fields
            for result in results:
                assert "id" in result
                assert "title" in result
                assert "content" in result
                assert "score" in result
            
            # Verify the Supabase RPC call was made correctly
            mock_supabase.rpc.assert_called_once_with(
                "match_pages",
                {"query_embedding": [0.9, 0.1], "match_k": 3}
            )
            
            # Test with k=1
            mock_supabase.reset_mock()
            mock_db_result.execute.return_value.data = [
                {"id": 1, "title": "Page 1", "content": "Content 1", "score": 0.95}
            ]
            mock_supabase.rpc.return_value = mock_db_result
            
            results = similar_pages("test query", k=1)
            assert len(results) == 1
            mock_supabase.rpc.assert_called_once_with(
                "match_pages",
                {"query_embedding": [0.9, 0.1], "match_k": 1}
            )