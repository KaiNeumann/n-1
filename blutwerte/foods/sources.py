"""
Source tracking utilities for food data.

All food-related data (nutrition, effects, biomarker correlations) must include
source references to ensure traceability and scientific validity.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional
from datetime import datetime


@dataclass
class DataSource:
    """
    Source reference for food data (nutrition, effects, etc.)
    
    Attributes:
        url: URL to the source (DOI, research paper, database, etc.)
        title: Human-readable title/description of the source
        source_type: Type of source for categorization
        access_date: When the source was accessed (ISO format: YYYY-MM-DD)
        doi: Digital Object Identifier for research papers
    """
    url: str
    title: str
    source_type: str  # "research", "database", "guideline", "government"
    access_date: Optional[str] = None
    doi: Optional[str] = None
    
    def __post_init__(self):
        """Set default access date if not provided"""
        if self.access_date is None:
            self.access_date = datetime.now().strftime("%Y-%m-%d")


@dataclass
class SourcedValue:
    """
    Any value with its source reference(s).
    
    Used when a single value needs explicit source tracking.
    
    Attributes:
        value: The actual value
        sources: List of sources supporting this value
    """
    value: Any
    sources: List[DataSource] = field(default_factory=list)


def create_source(url: str, title: str, source_type: str = "research") -> DataSource:
    """
    Factory function to create a DataSource with current date.
    
    Args:
        url: Source URL
        title: Source title
        source_type: Type of source (research, database, guideline, government)
        
    Returns:
        DataSource instance
        
    Example:
        >>> source = create_source(
        ...     "https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/",
        ...     "Vitamin K Fact Sheet",
        ...     "guideline"
        ... )
    """
    return DataSource(
        url=url,
        title=title,
        source_type=source_type,
        access_date=datetime.now().strftime("%Y-%m-%d")
    )


def validate_source(source: DataSource) -> bool:
    """
    Check if a source has required fields.
    
    Args:
        source: DataSource to validate
        
    Returns:
        True if valid, raises ValueError otherwise
        
    Raises:
        ValueError: If required fields are missing
    """
    if not source.url:
        raise ValueError("Source must have a URL")
    if not source.title:
        raise ValueError("Source must have a title")
    if source.source_type not in ("research", "database", "guideline", "government"):
        raise ValueError(f"Invalid source_type: {source.source_type}")
    return True
