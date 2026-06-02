# 🚀 FooDB Enrichment - Quick Start Guide

Ready to enrich your 8,419 foods with biomarker effects from FooDB? Follow these steps!

## Step 1: Download FooDB Data (87 MB)

### Option A: Automatic Download (Easiest)
```bash
python download_foodb.py
```
This will:
- Download FooDB JSON (~87 MB)
- Extract to `data/foodb/`
- Verify the setup

### Option B: Manual Download
1. Visit: https://foodb.ca/downloads
2. Download: **FooDB JSON file** (~87 MB) - this is the fastest option
3. Extract to: `data/foodb/FooDB.json`

## Step 2: Test the Setup

```bash
python quickstart_foodb.py
```

This will:
- ✓ Verify FooDB is installed
- ✓ Load the data
- ✓ Show a demo search for "spinach"
- ✓ Display biomarker mappings

Expected output:
```
✓ FooDB found: data/foodb/FooDB.json
✓ Imports successful
✓ Loaded 797 foods with 70926 compounds
Demo: Searching for 'spinach'...
✓ Found: Spinach
  Scientific name: Spinacia oleracea
  Group: Vegetables
  Compounds: 156
```

## Step 3: Enrich Your Foods

### Test on 10 foods first:
```bash
python enrich_foods_with_foodb.py --limit 10
```

### Then process all 8,419 foods:
```bash
python enrich_foods_with_foodb.py
```

This will:
1. Load your 8,419 legacy foods
2. Match them to FooDB foods (by name)
3. Extract bioactive compounds
4. Map compounds to biomarker effects
5. Add `FoodEffect` objects to each food
6. Save enriched foods to `enriched_foods/`

**Expected time:** 5-15 minutes depending on your system

## What Gets Enriched?

Your foods will get biomarker effects for:

### Compound Classes Mapped to Biomarkers:
- **Flavonoids** → CRP, IL-6, TNF-alpha (↓ inflammation)
- **Phytosterols** → LDL cholesterol (↓ 8-10% reduction)
- **Catechins** → Blood pressure, LDL oxidation (↓)
- **Carotenoids** → Vitamin A, antioxidant status (↑)
- **Phenolic acids** → Glucose, insulin (↓)
- **And 11 more classes...**

### Specific Nutrients:
- Iron, Vitamin B12, Folate, Vitamin D, Vitamin K
- Calcium, Magnesium, Zinc, Potassium
- EPA/DHA (Omega-3s)
- Dietary fiber

## Expected Results

Based on FooDB matching, you should see:
- **30-50% of foods matched** to FooDB entries
- **2-5 biomarker effects per matched food**
- **15-20 different biomarkers** covered across all foods

Example enrichment:
```
Food: Spinach
- Flavonoids → CRP, IL-6, TNF-alpha (decrease)
- Carotenoids → Vitamin A (increase)
- Phenolic acids → Glucose (decrease)
- Iron → Iron, Ferritin (increase)
- Vitamin K → Vitamin K (increase)
- Folate → Folic Acid (increase)
```

## Output Files

After enrichment, you'll have:

```
enriched_foods/
├── foods_enriched.py          # Python module with enriched foods
├── enrichment_stats.json      # Statistics and coverage report
└── unmatched_foods.txt        # Foods that couldn't be matched
```

The `enrichment_stats.json` will show:
- Total foods processed
- Foods successfully enriched
- Biomarker coverage counts
- Unmatched foods list

## Troubleshooting

### "FooDB data not found"
Run: `python download_foodb.py`

### "Import error"
Make sure you're in the project root directory and your virtual environment is activated.

### "No foods matched"
This is normal for some foods. FooDB has 797 foods, so not all 8,419 will match.
- Typical match rate: 30-50%
- Foods with scientific names match better
- Common foods (apples, spinach, etc.) match well

### Memory issues
FooDB JSON is ~87 MB but expands to ~500 MB in memory.
- Close other applications
- Use CSV format instead (slower but uses less memory)

## Advanced Usage

### Custom output directory:
```bash
python enrich_foods_with_foodb.py --output my_enriched_foods/
```

### Process specific food categories only:
Modify `enrich_foods_with_foodb.py` to filter by `food.category`.

### Add custom compound mappings:
Edit `blutwerte/foods/importers/foodb_mapping.py`:
```python
COMPOUND_CLASS_TO_BIOMARKERS["YourClass"] = {
    "biomarkers": ["YourBiomarker"],
    "direction": "increase",
    "mechanism": "Your mechanism",
    "evidence": "strong"
}
```

## Next Steps After Enrichment

1. **Review the enriched foods** in `enriched_foods/foods_enriched.py`
2. **Check statistics** in `enriched_foods/enrichment_stats.json`
3. **Integrate** the enriched foods back into your main database
4. **Use the effects** in your FoodAnalyzer

## Data Sources & Licensing

- **FooDB**: https://foodb.ca/ (CC BY-NC 4.0 for academic use)
- **Free for**: Research, education, personal use
- **Commercial use**: Requires license from FooDB

## Files Reference

| File | Purpose |
|------|---------|
| `download_foodb.py` | Downloads FooDB data |
| `quickstart_foodb.py` | Tests FooDB setup |
| `enrich_foods_with_foodb.py` | Main enrichment script |
| `blutwerte/foods/importers/foodb.py` | FooDB importer class |
| `blutwerte/foods/importers/foodb_mapping.py` | Biomarker mappings |
| `blutwerte/foods/importers/foodb_example.py` | Usage examples |
| `FOODB_INTEGRATION.md` | Full documentation |

## Questions?

Check `FOODB_INTEGRATION.md` for detailed documentation on:
- FooDB data structure
- API usage (optional)
- Compound-biomarker mappings
- Integration examples

---

**Ready to start?** Run:
```bash
python download_foodb.py && python quickstart_foodb.py
```
