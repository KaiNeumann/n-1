# N=1 Global TODO

This file tracks future enhancements, ideas, and technical debt for the n-1 project (formerly Blutwerte).

## 🎯 High Priority

### Food System Enhancements
- [ ] **Bioavailability Modeling**
  - Implement vitamin C + iron absorption synergy
  - Calcium-iron competition model
  - Fat-soluble vitamin absorption (A, D, E, K) with dietary fat
  - Phytate and tannin inhibition calculations

- [ ] **Preparation Method Effects**
  - Raw vs cooked spinach (oxalate changes)
  - Steaming vs boiling nutrient retention
  - Fermentation effects (sauerkraut, kimchi)
  - Cooking oil additions (fat content changes)

- [ ] **Meal Timing Effects**
  - Chronobiology: morning vs evening food effects
  - Post-workout nutrition timing
  - Fasting state absorption differences

### Activity System Expansion
- [ ] **More Activities**
  - Walking (various speeds)
  - Team sports (soccer, basketball)
  - Martial arts
  - Dancing
  - Hiking
  - Elliptical training
  - Rowing
  - Rock climbing

- [ ] **Activity Analyzer**
  - Analyze multiple sessions over time
  - Training load calculation
  - Recovery recommendations
  - Overtraining detection

- [ ] **Individual Fitness Adjustment**
  - Trained vs untrained responses
  - Age-adjusted effects
  - Gender differences
  - VO2 max correlation

### Data Completeness
- [ ] **Add Biomarker Effects to Legacy Foods**
  - Identify top 100 foods by usage/importance
  - Add vitamin K effects to leafy greens
  - Add iron effects to red meat, legumes
  - Add calcium effects to dairy
  - Research and document effects with sources

## 🔄 Medium Priority

### Recipe & Meal Planning
- [ ] **Recipe Composition**
  - Create recipes from multiple foods
  - Automatic nutrition calculation
  - Portion scaling for recipes
  - Recipe import from external sources

- [ ] **Weekly Meal Planning**
  - Plan meals with biomarker optimization
  - "Boost iron this week" recommendations
  - Shopping list generation
  - Meal prep scheduling

- [ ] **Food Combination Analysis**
  - Synergistic effects (vitamin C + iron)
  - Antagonistic effects (calcium + iron)
  - Optimal meal composition

### Patient Integration
- [ ] **Patient Profile Integration**
  - Load patient YAML files
  - Track foods and activities alongside blood tests
  - Correlate intake with biomarker trends
  - Personalized recommendations

- [ ] **Historical Tracking**
  - Food intake history
  - Activity session history
  - Trend analysis over months/years
  - Seasonal pattern detection

### Data Import/Export
- [ ] **More Importers**
  - MyFitnessPal export import
  - Apple Health/Google Fit integration
  - Fitbit activity data
  - Garmin Connect

- [ ] **Export Capabilities**
  - PDF reports for doctors
  - CSV exports for analysis
  - JSON API for integrations

## 🔬 Research & Evidence

### Biomarker Effects to Research
- [ ] **Inflammatory Markers**
  - CRP effects of various foods (omega-3, turmeric, etc.)
  - Exercise-induced inflammation patterns
  - Anti-inflammatory diet scoring

- [ ] **Lipid Profile**
  - Saturated fat effects (individual variation)
  - Fiber effects on cholesterol
  - Omega-3 fatty acid impacts

- [ ] **Glycemic Control**
  - Glycemic index/load integration
  - Fiber effects on glucose
  - Post-meal glucose curves

- [ ] **Kidney Function**
  - Protein intake and creatinine
  - Sodium effects on kidney markers
  - Hydration biomarkers

- [ ] **Liver Function**
  - Alcohol effects on liver enzymes
  - NAFLD dietary factors
  - Medication interactions

## 🛠 Technical Improvements

### Code Quality
- [ ] **Type Checking**
  - Full mypy type coverage
  - Runtime type validation
  - Better type hints for dynamic data

- [ ] **Testing**
  - Integration tests for importers
  - Mock external API calls
  - Performance tests for large datasets
  - Test coverage > 90%

- [ ] **Documentation**
  - API reference docs
  - Contributing guidelines
  - Architecture documentation
  - Tutorial notebooks

### Performance
- [ ] **Database Optimization**
  - FoodDatabase: Add more indexes
  - Lazy loading for large datasets
  - Caching for frequent queries
  - Database persistence (SQLite/PostgreSQL)

- [ ] **Analysis Speed**
  - Parallel processing for large food lists
  - Optimize biomarker lookups
  - Cache RDI calculations

## 🌍 Internationalization

- [ ] **Multi-language Support**
  - English names for all foods
  - French food database (CIQUAL)
  - USDA FoodData Central integration
  - Localized portion names

- [ ] **Regional Databases**
  - UK food database
  - Australian food database
  - Nordic food database
  - Asian food databases

## 🔮 Future Concepts

### Machine Learning
- [ ] **Personalized Predictions**
  - Predict biomarker changes from intake
  - Individual response models
  - Anomaly detection

- [ ] **Recommendation Engine**
  - "If you eat X, expect Y in your blood work"
  - Optimal diet for specific biomarkers
  - Intervention suggestions

### Advanced Features
- [ ] **Supplement Tracking**
  - Track supplement intake
  - Interaction checking
  - Optimal timing recommendations

- [ ] **Sleep Integration**
  - Sleep quality effects on biomarkers
  - Meal timing relative to sleep
  - Circadian rhythm optimization

- [ ] **Stress Tracking**
  - Cortisol patterns
  - Stress biomarkers
  - Recovery metrics

- [ ] **Gut Health**
  - Probiotic effects
  - Prebiotic fiber tracking
  - Microbiome correlations

## 🐛 Known Issues & Technical Debt

### Migration Cleanup
- [ ] **Legacy Files to Remove**
  - food_legacy/ directory (all migrated)
  - migrate_legacy_foods.py (one-time use)
  - convert_bls_to_python.py (one-time use)
  - food_bls_german.py (generated, now migrated)

### Code Cleanup
- [ ] **Refactor Legacy Importer Code**
  - Remove sys.path.insert patterns
  - Update to new API patterns
  - Better error handling

- [ ] **Fix Arithmetic Parsing**
  - 19 foods had unparsable calculations
  - Fix division/multiplication in legacy files
  - Handle these in migration script

## 📊 Data Sources to Add

### Priority Databases
1. **USDA FoodData Central** - Complete integration (not just references)
2. **CIQUAL (France)** - French food composition
3. **FSANZ (Australia/NZ)** - Australian database
4. **Livsmedelsverket (Sweden)** - Swedish database
5. **THL (Finland)** - Finnish database

### Specialty Databases
- **Organic foods database**
- **Restaurant chain nutrition data**
- **International cuisines** (Indian, Chinese, Mexican)
- **Specialty diets** (keto, paleo, vegan alternatives)

## 🎨 User Experience

### Visualization
- [ ] **Charts & Graphs**
  - Biomarker trends over time
  - Nutrition intake visualizations
  - Activity vs biomarker correlations
  - Meal composition pie charts

### Mobile App Ideas
- [ ] **Photo-based Food Logging**
  - Take photo → AI identifies food
  - Barcode scanning for packaged foods
  - Voice logging

- [ ] **Smart Notifications**
  - "Your iron is low, consider spinach"
  - Post-workout recovery reminders
  - Blood test preparation tips

## 🏥 Medical Integration

### Clinical Features
- [ ] **Lab Result Import**
  - HL7 FHIR integration
  - PDF lab report parsing
  - Direct lab API connections

- [ ] **Clinical Decision Support**
  - Alert on dangerous combinations
  - Drug-food interaction checking
  - Condition-specific recommendations

### Research
- [ ] **Cohort Studies**
  - Aggregate anonymized data
  - Population-level insights
  - Research collaborations

## 🤝 Community

- [ ] **Open Source**
  - Publish on GitHub
  - Contributor guidelines
  - Code of conduct
  - License clarification

- [ ] **Community Database**
  - User-contributed foods
  - Verification system
  - Regional specialties

## 📅 Timeline Ideas

### Phase 1 (Next 3 months)
- Complete bioavailability modeling for top 10 nutrients
- Add biomarker effects to top 100 foods
- Create ActivityAnalyzer
- Clean up legacy code

### Phase 2 (3-6 months)
- Recipe system
- Patient profile integration
- Full USDA FDC integration
- Testing > 90% coverage

### Phase 3 (6-12 months)
- Machine learning predictions
- Mobile app prototype
- International expansion
- Research partnerships

---

## 📝 Contributing

To add items to this TODO:
1. Create a branch
2. Add your idea under appropriate section
3. Include context and rationale
4. Submit PR with label "enhancement"

## 🏆 Completed Items

- [x] Migration of 8,419 foods from legacy system
- [x] Portion system implementation
- [x] Source tracking for all data
- [x] 5 importers (OFF, BLS, FDDB, Nutritionix, Yazio)
- [x] Activities module as top-level entity
- [x] 6 activities with biomarker effects
- [x] Comprehensive test suite
- [x] Documentation (README, MIGRATION.md)

---

*Last updated: 2026-02-19*
*Next review: 2026-03-19*
