from src.etl.transformers.ip_transformer import IPLocationTransformer


class TestIPLocationTransformer:
    """Test IP data transformation and validation"""

    def test_transforms_valid_data(self):
        """Should successfully transform valid IP data"""
        transformer = IPLocationTransformer()
        raw_data = [
            {
                "start_ip": "1.0.0.0",
                "end_ip": "1.0.0.255",
                "country": "Australia",
                "city": "Sydney",
            }
        ]

        result = transformer.transform(raw_data)

        assert len(result) == 1
        assert result[0]["start_ip"] == "1.0.0.0"
        assert result[0]["end_ip"] == "1.0.0.255"
        assert result[0]["country"] == "Australia"
        assert result[0]["city"] == "Sydney"

    def test_skips_invalid_ip_addresses(self):
        """Should skip records with invalid IP addresses"""
        transformer = IPLocationTransformer()
        raw_data = [
            {
                "start_ip": "invalid.ip",
                "end_ip": "1.0.0.255",
                "country": "Australia",
                "city": "Sydney",
            },
            {
                "start_ip": "2.0.0.0",
                "end_ip": "2.0.0.255",
                "country": "France",
                "city": "Paris",
            },
        ]

        result = transformer.transform(raw_data)

        # Should only include the valid record
        assert len(result) == 1
        assert result[0]["start_ip"] == "2.0.0.0"

    def test_skips_invalid_ip_ranges(self):
        """Should skip records where start_ip > end_ip"""
        transformer = IPLocationTransformer()
        raw_data = [
            {
                "start_ip": "2.0.0.0",
                "end_ip": "1.0.0.0",  # Invalid: start > end
                "country": "Test",
                "city": "Test",
            }
        ]

        result = transformer.transform(raw_data)

        assert len(result) == 0

    def test_skips_empty_location_fields(self):
        """Should skip records with empty country or city"""
        transformer = IPLocationTransformer()
        raw_data = [
            {
                "start_ip": "1.0.0.0",
                "end_ip": "1.0.0.255",
                "country": "",  # Empty
                "city": "Sydney",
            },
            {
                "start_ip": "2.0.0.0",
                "end_ip": "2.0.0.255",
                "country": "France",
                "city": "",  # Empty
            },
        ]

        result = transformer.transform(raw_data)

        assert len(result) == 0

    def test_cleans_whitespace(self):
        """Should clean whitespace from fields"""
        transformer = IPLocationTransformer()
        raw_data = [
            {
                "start_ip": " 1.0.0.0 ",
                "end_ip": " 1.0.0.255 ",
                "country": " Australia ",
                "city": " Sydney ",
            }
        ]

        result = transformer.transform(raw_data)

        assert len(result) == 1
        assert result[0]["start_ip"] == "1.0.0.0"
        assert result[0]["end_ip"] == "1.0.0.255"
        assert result[0]["country"] == "Australia"
        assert result[0]["city"] == "Sydney"
