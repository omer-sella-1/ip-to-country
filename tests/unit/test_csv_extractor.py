import os
import tempfile

import pytest

from src.etl.extractors.csv_extractor import CSVExtractor


class TestCSVExtractor:
    """Test CSV data extraction functionality"""

    def test_extracts_valid_csv_data(self):
        """Should extract data from properly formatted CSV"""
        # Create temporary CSV file
        csv_content = """start_ip,end_ip,country,city
1.0.0.0,1.0.0.255,Australia,Sydney
2.0.0.0,2.0.0.255,France,Paris"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            extractor = CSVExtractor(temp_path)
            result = extractor.extract()

            assert len(result) == 2
            assert result[0]["start_ip"] == "1.0.0.0"
            assert result[0]["country"] == "Australia"
            assert result[1]["start_ip"] == "2.0.0.0"
            assert result[1]["country"] == "France"
        finally:
            os.unlink(temp_path)

    def test_raises_error_for_missing_headers(self):
        """Should raise error when required headers are missing"""
        csv_content = """start_ip,end_ip,location
1.0.0.0,1.0.0.255,Australia"""  # Missing 'country' and 'city'

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            extractor = CSVExtractor(temp_path)

            with pytest.raises(ValueError, match="CSV missing headers"):
                extractor.extract()
        finally:
            os.unlink(temp_path)

    def test_skips_empty_rows(self):
        """Should skip rows with empty required fields"""
        csv_content = """start_ip,end_ip,country,city
1.0.0.0,1.0.0.255,Australia,Sydney
,,France,Paris
2.0.0.0,2.0.0.255,France,"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            extractor = CSVExtractor(temp_path)
            result = extractor.extract()

            # Should only include the first valid row
            assert len(result) == 1
            assert result[0]["country"] == "Australia"
        finally:
            os.unlink(temp_path)

    def test_cleans_whitespace_from_fields(self):
        """Should clean whitespace from CSV fields"""
        csv_content = """start_ip,end_ip,country,city
 1.0.0.0 , 1.0.0.255 , Australia , Sydney """

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            temp_path = f.name

        try:
            extractor = CSVExtractor(temp_path)
            result = extractor.extract()

            assert len(result) == 1
            assert result[0]["start_ip"] == "1.0.0.0"
            assert result[0]["end_ip"] == "1.0.0.255"
            assert result[0]["country"] == "Australia"
            assert result[0]["city"] == "Sydney"
        finally:
            os.unlink(temp_path)

    def test_get_source_info(self):
        """Should return correct source information"""
        extractor = CSVExtractor("/path/to/test.csv")

        result = extractor.get_source_info()

        assert result == "CSV file: /path/to/test.csv"
