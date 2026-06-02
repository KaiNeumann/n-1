"""
core.medications.jsonl_loader

Loads Medication objects from knowledge/medications/medications.jsonl.
Falls back to the Python source in core/medications/data/*.py
when the JSONL is missing or empty.

Public API:
    load_medications_from_jsonl(path=None) -> Dict[str, Medication]
    load_medications_from_python()         -> Dict[str, Medication]
    load_medications(source='auto')        -> Dict[str, Medication]
"""

from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List

from .._jsonl import read_jsonl
from .effects.dose_models import DoseEffectModel, DoseEffectRange
from .models import (
    DrugInteraction,
    EffectDirection,
    EffectTargetType,
    FrequencyCategory,
    Medication,
    MedicationEffect,
    MonitoringRequirement,
    Quote,
    RiskFactor,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSONL = REPO_ROOT / "knowledge" / "medications" / "medications.jsonl"


def _row_to_quote(row: dict) -> Quote:
    return Quote(
        text=row.get("text", ""),
        source=row.get("source", ""),
        source_type=row.get("source_type", "research"),
    )


def _row_to_risk_factor(row: dict) -> RiskFactor:
    kwargs = dict(row)
    rng = kwargs.pop("biomarker_range", None)
    if rng is not None:
        kwargs["biomarker_range"] = tuple(rng)
    return RiskFactor(**kwargs)


def _row_to_dose_range(row: dict) -> DoseEffectRange:
    return DoseEffectRange(
        min_dose=row.get("min_dose", 0.0),
        max_dose=row.get("max_dose", 0.0),
        dose_unit=row.get("dose_unit", "mg"),
        frequency_percentage=row.get("frequency_percentage", 0.0),
        magnitude=row.get("magnitude", "mild"),
        description=row.get("description", ""),
    )


def _row_to_dose_model(row: dict) -> DoseEffectModel:
    if not row:
        return None
    points = row.get("dose_response_points")
    if points:
        points = [tuple(p) for p in points]
    return DoseEffectModel(
        model_type=row.get("model_type", "approximate"),
        typical_max_dose=row.get("typical_max_dose"),
        low_dose=_row_to_dose_range(row["low_dose"]) if row.get("low_dose") else None,
        medium_dose=_row_to_dose_range(row["medium_dose"]) if row.get("medium_dose") else None,
        high_dose=_row_to_dose_range(row["high_dose"]) if row.get("high_dose") else None,
        dose_response_points=points,
        threshold_dose=row.get("threshold_dose"),
        threshold_unit=row.get("threshold_unit"),
        above_threshold_effect=row.get("above_threshold_effect"),
        above_threshold_frequency=row.get("above_threshold_frequency"),
    )


def _enum_or_none(enum_cls, value, default=None):
    if value is None:
        return default
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(value)
    except (TypeError, ValueError):
        for member in enum_cls:
            if member.value == value:
                return member
        return default


def _row_to_medication_effect(row: dict) -> MedicationEffect:
    return MedicationEffect(
        target_type=_enum_or_none(EffectTargetType, row.get("target_type"), EffectTargetType.BIOMARKER),
        target_name=row.get("target_name", ""),
        direction=_enum_or_none(EffectDirection, row.get("direction"), EffectDirection.NONE),
        typical_magnitude=row.get("typical_magnitude", "mild"),
        frequency_category=_enum_or_none(FrequencyCategory, row.get("frequency_category"), FrequencyCategory.COMMON),
        target_synonyms=row.get("target_synonyms", []) or [],
        dose_dependent=bool(row.get("dose_dependent", False)),
        dose_model=_row_to_dose_model(row.get("dose_model")),
        frequency_percentage=row.get("frequency_percentage"),
        time_to_onset=row.get("time_to_onset", "days"),
        duration=row.get("duration", "persistent"),
        administration_time_relevant=bool(row.get("administration_time_relevant", False)),
        mechanism=row.get("mechanism", ""),
        clinical_significance=row.get("clinical_significance", "expected"),
        requires_monitoring=bool(row.get("requires_monitoring", False)),
        monitoring_recommendation=row.get("monitoring_recommendation", ""),
        risk_factors=[_row_to_risk_factor(r) for r in (row.get("risk_factors") or [])],
        protective_factors=row.get("protective_factors", []) or [],
        evidence=[_row_to_quote(q) for q in (row.get("evidence") or [])],
        likelihood_score=row.get("likelihood_score", ""),
        symptom_description=row.get("symptom_description", ""),
        outcome_metric=row.get("outcome_metric", ""),
        outcome_timeframe=row.get("outcome_timeframe", ""),
    )


def _row_to_drug_interaction(row: dict) -> DrugInteraction:
    return DrugInteraction(
        interacting_drug=row.get("interacting_drug", ""),
        severity=row.get("severity", "moderate"),
        effect_description=row.get("effect_description", ""),
        mechanism=row.get("mechanism", ""),
        management=row.get("management", ""),
        evidence=[_row_to_quote(q) for q in (row.get("evidence") or [])],
    )


def _row_to_monitoring(row: dict) -> MonitoringRequirement:
    return MonitoringRequirement(
        target_type=EffectTargetType(row.get("target_type", "biomarker")),
        target_name=row.get("target_name", ""),
        baseline_required=bool(row.get("baseline_required", True)),
        frequency=row.get("frequency", ""),
        condition=row.get("condition", ""),
    )


def _row_to_medication(row: dict) -> Medication:
    doses = row.get("available_doses") or []
    doses = [tuple(d) for d in doses]
    typical = row.get("typical_dose_range")
    if typical is not None:
        typical = tuple(typical)
    return Medication(
        name=row.get("name", ""),
        name_de=row.get("name_de", ""),
        brand_names=row.get("brand_names", []) or [],
        synonyms=row.get("synonyms", []) or [],
        drug_class=row.get("drug_class", ""),
        drug_subclass=row.get("drug_subclass", ""),
        available_doses=doses,
        typical_dose_range=typical,
        effects=[_row_to_medication_effect(e) for e in (row.get("effects") or [])],
        indications=[_row_to_quote(q) for q in (row.get("indications") or [])],
        contraindications=[_row_to_quote(q) for q in (row.get("contraindications") or [])],
        black_box_warnings=[_row_to_quote(q) for q in (row.get("black_box_warnings") or [])],
        drug_interactions=[_row_to_drug_interaction(d) for d in (row.get("drug_interactions") or [])],
        monitoring_protocol=[_row_to_monitoring(m) for m in (row.get("monitoring_protocol") or [])],
        pregnancy_category=row.get("pregnancy_category", ""),
        requires_prescription=bool(row.get("requires_prescription", True)),
        controlled_substance=bool(row.get("controlled_substance", False)),
        primary_sources=[_row_to_quote(q) for q in (row.get("primary_sources") or [])],
        fda_label_url=row.get("fda_label_url", ""),
        ema_label_url=row.get("ema_label_url", ""),
        last_updated=row.get("last_updated", ""),
    )


def load_medications_from_jsonl(path: Path = None) -> Dict[str, Medication]:
    """Load medications from the JSONL knowledge file.

    Returns a dict keyed by medication name (lowercased), the same
    shape as MedicationDatabase._medications.
    """
    path = path or DEFAULT_JSONL
    out: Dict[str, Medication] = {}
    for row in read_jsonl(path):
        med = _row_to_medication(row)
        if med.name:
            out[med.name.lower()] = med
    return out


def load_medications_from_python() -> Dict[str, Medication]:
    """Load medications by walking core.medications.data."""
    from . import data as meds_data
    from .data import vitamins

    out: Dict[str, Medication] = {}
    modules: List = []
    for _, modname, _ in pkgutil.iter_modules(meds_data.__path__, meds_data.__name__ + "."):
        try:
            modules.append(importlib.import_module(modname))
        except Exception:
            continue
    try:
        for _, modname, _ in pkgutil.iter_modules(vitamins.__path__, vitamins.__name__ + "."):
            try:
                modules.append(importlib.import_module(modname))
            except Exception:
                continue
    except ImportError:
        pass

    for module in modules:
        for attr_name in dir(module):
            if not attr_name.startswith("create_"):
                continue
            func = getattr(module, attr_name, None)
            if not callable(func):
                continue
            try:
                med = func()
            except Exception:
                continue
            if isinstance(med, Medication):
                out[med.name.lower()] = med
    return out


def load_medications(source: str = "auto") -> Dict[str, Medication]:
    """Load medications, preferring JSONL when available.

    source: 'auto' (default) -> JSONL if it exists, else Python
            'jsonl'           -> JSONL only (raises if missing)
            'python'          -> Python only
    """
    if source == "python":
        return load_medications_from_python()
    if source == "jsonl":
        return load_medications_from_jsonl()

    if DEFAULT_JSONL.exists() and DEFAULT_JSONL.stat().st_size > 0:
        return load_medications_from_jsonl()
    return load_medications_from_python()
