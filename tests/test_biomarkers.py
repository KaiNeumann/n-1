"""
Basic tests for core library
"""

import pytest
from datetime import datetime
from core import (
    get_biomarker, 
    search_biomarkers, 
    list_biomarkers,
    Category,
    load_blood_tests
)


def test_get_biomarker_by_name():
    """Test lookup by primary name"""
    crp = get_biomarker("CRP")
    assert crp is not None
    assert crp.name == "CRP"
    assert crp.name_de == "C-reaktives Protein"


def test_get_biomarker_by_german_name():
    """Test lookup by German name"""
    crp = get_biomarker("C-reaktives Protein")
    assert crp is not None
    assert crp.name == "CRP"


def test_get_biomarker_by_lab_id():
    """Test lookup by lab ID"""
    crp = get_biomarker("A-CRPQ")
    assert crp is not None
    assert crp.name == "CRP"


def test_get_biomarker_not_found():
    """Test lookup of non-existent biomarker"""
    result = get_biomarker("NonExistent")
    assert result is None


def test_search_biomarkers():
    """Test search functionality"""
    results = search_biomarkers("Cholesterol")
    assert len(results) > 0
    names = [b.name for b in results]
    assert "Total Cholesterol" in names
    assert "HDL Cholesterol" in names


def test_list_biomarkers():
    """Test listing all biomarkers"""
    biomarkers = list_biomarkers()
    assert len(biomarkers) > 0
    assert "CRP" in biomarkers
    assert "Hemoglobin" in biomarkers


def test_biomarker_ranges():
    """Test that biomarkers have ranges"""
    crp = get_biomarker("CRP")
    assert "mg/l" in crp.ranges
    ranges = crp.ranges["mg/l"]
    assert len(ranges) > 0


def test_value_interpretation():
    """Test value interpretation"""
    crp = get_biomarker("CRP")
    
    # Normal value
    result = crp.interpret_value(0.5, "mg/l")
    assert result["status"] == "normal"
    
    # High value
    result = crp.interpret_value(3.5, "mg/l")
    assert result["status"] == "high"


def test_gender_specific_ranges():
    """Test gender-specific reference ranges"""
    hb = get_biomarker("Hemoglobin")
    
    # Female range
    female_result = hb.interpret_value(13.5, "g/dl", {"gender": "female"})
    male_result = hb.interpret_value(13.5, "g/dl", {"gender": "male"})
    
    assert female_result["status"] == "normal"
    # Same value might be interpreted differently for male


def test_csv_loading():
    """Test CSV loading"""
    try:
        history = load_blood_tests("blutbild.csv")
        assert len(history.records) > 0
        assert len(history.list_biomarkers()) > 0
        assert len(history.list_dates()) > 0
        
        # Test get_latest_value
        latest = history.get_latest_value("Cholesterin")
        assert latest is not None
        assert latest.value > 0
    except FileNotFoundError:
        pytest.skip("CSV file not found")


def test_timeline():
    """Test timeline functionality"""
    try:
        history = load_blood_tests("blutbild.csv")
        timeline = history.get_timeline("HbA1c")
        
        if timeline:
            # Should be sorted by date
            dates = [t[0] for t in timeline]
            assert dates == sorted(dates)
    except FileNotFoundError:
        pytest.skip("CSV file not found")


def test_get_records_for_date():
    """Test getting records for specific date"""
    try:
        history = load_blood_tests("blutbild.csv")
        dates = history.list_dates()
        
        if dates:
            records = history.get_records_for_date(dates[0])
            assert len(records) > 0
            for r in records:
                assert r.date == dates[0]
    except FileNotFoundError:
        pytest.skip("CSV file not found")


def test_biomarker_categories():
    """Test biomarker categories"""
    from core.bloodtests.biomarkers_db import _db
    
    enzymes = _db.by_category(Category.ENZYMES)
    assert len(enzymes) > 0
    
    lipids = _db.by_category(Category.LIPIDS)
    assert len(lipids) > 0


def test_biomarker_all_names():
    """Test getting all names for biomarker"""
    crp = get_biomarker("CRP")
    names = crp.get_all_names()
    
    assert "CRP" in names
    assert "C-reaktives Protein" in names
    assert "A-CRPQ" in names  # Lab ID in synonyms


def test_export_to_dict():
    """Test exporting biomarker to dict"""
    crp = get_biomarker("CRP")
    data = crp.to_dict()
    
    assert "name" in data
    assert "name_de" in data
    assert "ranges" in data
    assert data["name"] == "CRP"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
