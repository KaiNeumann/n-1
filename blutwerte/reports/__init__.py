"""
PDF Report Generation Module

Generates comprehensive health reports in PDF format.

Example Usage:
    >>> from blutwerte.reports import HealthReportGenerator
    >>> 
    >>> generator = HealthReportGenerator(
    ...     user_name="John Doe",
    ...     user_id="user001"
    ... )
    >>> 
    >>> # Add data
    >>> generator.add_diary_data(diary)
    >>> generator.add_blood_tests(blood_tests)
    >>> generator.add_goals(goal_manager)
    >>> generator.add_correlations(correlation_engine)
    >>> 
    >>> # Generate PDF
    >>> generator.generate_pdf("health_report.pdf")
"""

from datetime import datetime, date, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from fpdf import FPDF
import os


@dataclass
class ReportSection:
    """A section of the report."""
    title: str
    content: str
    level: int = 1  # 1=chapter, 2=section, 3=subsection


class PDFReport(FPDF):
    """Custom PDF report class."""
    
    def __init__(self):
        super().__init__()
        self.chapter_title = ""
        
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Blutwerte Health Report', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


class HealthReportGenerator:
    """
    Generates comprehensive health PDF reports.
    """
    
    def __init__(
        self,
        user_name: str,
        user_id: str,
        title: str = "Comprehensive Health Report",
    ):
        self.user_name = user_name
        self.user_id = user_id
        self.title = title
        
        self.diary = None
        self.blood_tests = []
        self.goal_manager = None
        self.correlation_engine = None
        self.medication_diary = None
        self.insights = []
        
        self.report_date = date.today()
    
    def add_diary_data(self, diary):
        """Add diary data to report."""
        self.diary = diary
    
    def add_blood_tests(self, blood_tests):
        """Add blood test results."""
        self.blood_tests = blood_tests
    
    def add_goals(self, goal_manager):
        """Add goal manager."""
        self.goal_manager = goal_manager
    
    def add_correlations(self, engine):
        """Add correlation engine."""
        self.correlation_engine = engine
    
    def add_medication_diary(self, med_diary):
        """Add medication diary."""
        self.medication_diary = med_diary
    
    def add_insights(self, insights: List):
        """Add insights to report."""
        self.insights = insights
    
    def generate_pdf(self, filepath: str) -> str:
        """Generate the PDF report."""
        pdf = PDFReport()
        pdf.add_page()
        
        # Title page
        self._generate_title_page(pdf)
        
        # Executive summary
        self._generate_summary(pdf)
        
        # Blood test results
        self._generate_blood_tests(pdf)
        
        # Goals and progress
        self._generate_goals(pdf)
        
        # Diary overview
        self._generate_diary(pdf)
        
        # Medication summary
        self._generate_medications(pdf)
        
        # Insights and recommendations
        self._generate_insights(pdf)
        
        # Correlation analysis
        self._generate_correlations(pdf)
        
        # Use cases section (large section)
        self._generate_use_cases(pdf)
        
        # Save
        pdf.output(filepath)
        return filepath
    
    def _generate_title_page(self, pdf: PDFReport):
        """Generate title page."""
        pdf.ln(40)
        
        pdf.set_font('Helvetica', 'B', 24)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 20, self.title, 0, 1, 'C')
        
        pdf.ln(10)
        
        pdf.set_font('Helvetica', '', 14)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 10, f"Prepared for: {self.user_name}", 0, 1, 'C')
        pdf.cell(0, 10, f"User ID: {self.user_id}", 0, 1, 'C')
        pdf.cell(0, 10, f"Report Date: {self.report_date.strftime('%B %d, %Y')}", 0, 1, 'C')
        
        pdf.ln(20)
        pdf.set_font('Helvetica', 'I', 10)
        pdf.multi_cell(0, 6, "This report provides a comprehensive overview of your health data, "
                          "including blood test results, daily tracking, goals progress, "
                          "and personalized insights.", 0, 'C')
        
        pdf.add_page()
    
    def _generate_summary(self, pdf: PDFReport):
        """Generate executive summary."""
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "Executive Summary", 0, 1)
        pdf.ln(2)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        summary_items = []
        
        # Blood tests
        if self.blood_tests:
            summary_items.append(f"- {len(self.blood_tests)} blood test record(s) analyzed")
        
        # Goals
        if self.goal_manager:
            dash = self.goal_manager.get_dashboard_summary()
            summary_items.append(f"- {dash['active_goals']} active health goals")
            summary_items.append(f"- {dash['milestones_achieved']} milestones achieved")
        
        # Diary
        if self.diary:
            summary_items.append(f"- {len(self.diary.entries)} diary entries recorded")
        
        # Insights
        if self.insights:
            high_priority = len([i for i in self.insights if getattr(i, 'priority', '') == 'high'])
            summary_items.append(f"- {len(self.insights)} insights generated ({high_priority} high priority)")
        
        for item in summary_items:
            pdf.cell(0, 8, item, 0, 1)
        
        pdf.ln(5)
    
    def _generate_blood_tests(self, pdf: PDFReport):
        """Generate blood test section."""
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "Blood Test Results", 0, 1)
        pdf.ln(2)
        
        if not self.blood_tests:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "No blood test data available.", 0, 1)
            return
        
        # Group by date
        for bt in self.blood_tests:
            bt_date = getattr(bt, 'date', None)
            if hasattr(bt_date, 'strftime'):
                date_str = bt_date.strftime('%B %d, %Y')
            else:
                date_str = str(bt_date)
            
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, f"Date: {date_str}", 0, 1)
            
            pdf.set_font('Helvetica', '', 9)
            
            # List all numeric attributes
            for attr in ['ldl', 'hdl', 'triglycerides', 'total_cholesterol', 
                        'glucose', 'hba1c', 'vitamin_d', 'ferritin', 'crp',
                        'bp_systolic', 'bp_diastolic']:
                value = getattr(bt, attr, None)
                if value is not None and value != 0:
                    pdf.cell(0, 6, f"  {attr.replace('_', ' ').title()}: {value}", 0, 1)
            
            pdf.ln(3)
    
    def _generate_goals(self, pdf: PDFReport):
        """Generate goals and progress section."""
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "Goals & Progress", 0, 1)
        pdf.ln(2)
        
        if not self.goal_manager:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "No goals set.", 0, 1)
            return
        
        goals = self.goal_manager.get_active_goals()
        
        pdf.set_font('Helvetica', '', 10)
        
        for goal in goals:
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 8, f"Goal: {goal.name}", 0, 1)
            
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(80, 80, 80)
            
            target_str = f"Target: {goal.target_value} {goal.unit}"
            if goal.start_value:
                target_str += f" (started at {goal.start_value})"
            pdf.cell(0, 6, target_str, 0, 1)
            
            priority_str = f"Priority: {goal.priority.value.title()}"
            pdf.cell(0, 6, priority_str, 0, 1)
            
            pdf.ln(2)
        
        # Milestones
        if self.goal_manager.milestones:
            pdf.ln(5)
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(0, 51, 102)
            pdf.cell(0, 8, "Milestones Achieved", 0, 1)
            
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(0, 0, 0)
            
            for m in self.goal_manager.milestones[-10:]:  # Last 10
                pdf.cell(0, 6, f"- {m.milestone_type.value.replace('_', ' ').title()}", 0, 1)
    
    def _generate_diary(self, pdf: PDFReport):
        """Generate diary overview."""
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "Daily Diary Overview", 0, 1)
        pdf.ln(2)
        
        if not self.diary or not self.diary.entries:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "No diary entries recorded.", 0, 1)
            return
        
        # Get metrics summary
        metrics = self.diary.get_metrics()
        
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, f"Total entries: {len(self.diary.entries)}", 0, 1)
        pdf.cell(0, 8, f"Unique metrics tracked: {len(metrics)}", 0, 1)
        pdf.ln(5)
        
        # Recent entries
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "Recent Entries", 0, 1)
        
        pdf.set_font('Helvetica', '', 8)
        
        recent = self.diary.get_entries(limit=15)
        for entry in recent:
            date_str = entry.timestamp.strftime('%m/%d %H:%M')
            value_str = str(entry.value)[:30]
            pdf.cell(0, 5, f"  {date_str} - {entry.metric}: {value_str}", 0, 1)
    
    def _generate_medications(self, pdf: PDFReport):
        """Generate medication summary."""
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "Medication & Supplement Summary", 0, 1)
        pdf.ln(2)
        
        if not self.medication_diary:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "No medication data available.", 0, 1)
            return
        
        # Schedules
        schedules = self.medication_diary.get_schedules(active_only=True)
        
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, "Active Medications & Supplements", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        for s in schedules:
            pdf.cell(0, 7, f"- {s.name} - {s.dosage} {s.unit} ({s.frequency.value})", 0, 1)
        
        # Today's intakes
        pdf.ln(5)
        today_intakes = self.medication_diary.get_today_intakes()
        
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, f"Today's Intakes: {len(today_intakes)}", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        for i in today_intakes:
            time_str = i.taken_at.strftime('%H:%M')
            pdf.cell(0, 6, f"  - {time_str} - {i.medication_name} ({i.dosage_taken} {i.unit})", 0, 1)
    
    def _generate_insights(self, pdf: PDFReport):
        """Generate insights section."""
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "Health Insights & Recommendations", 0, 1)
        pdf.ln(2)
        
        if not self.insights:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "No insights available yet. Continue tracking your data!", 0, 1)
            return
        
        for insight in self.insights[:15]:  # Limit to 15
            priority_color = {'high': (200, 0, 0), 'medium': (200, 150, 0), 'low': (0, 100, 0)}
            color = priority_color.get(getattr(insight, 'priority', 'low'), (0, 0, 0))
            
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(*color)
            pdf.cell(0, 8, f"[{getattr(insight, 'priority', 'low').upper()}] {insight.title}", 0, 1)
            
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(0, 0, 0)
            
            # Wrap message
            pdf.multi_cell(0, 5, insight.message[:300])
            
            if hasattr(insight, 'action_items') and insight.action_items:
                pdf.ln(2)
                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(0, 5, "Actions:", 0, 1)
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(80, 80, 80)
                for action in insight.action_items[:3]:
                    pdf.cell(0, 4, f"  - {action}", 0, 1)
            
            pdf.ln(5)
            pdf.set_text_color(0, 0, 0)
    
    def _generate_correlations(self, pdf: PDFReport):
        """Generate correlation analysis section."""
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "Biomarker Correlation Analysis", 0, 1)
        pdf.ln(2)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, "This section analyzes how your daily activities, diet, and medications "
                          "may be influencing your blood test biomarkers.")
        pdf.ln(5)
        
        if not self.correlation_engine or not self.blood_tests:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "Not enough data for correlation analysis. Continue tracking!", 0, 1)
            return
        
        # Analyze recent blood tests
        if len(self.blood_tests) >= 2:
            latest = self.blood_tests[-1]
            previous = self.blood_tests[-2]
            
            # Analyze LDL if available
            ldl_new = getattr(latest, 'ldl', None)
            ldl_old = getattr(previous, 'ldl', None)
            
            if ldl_new and ldl_old:
                result = self.correlation_engine.analyze_change(
                    'ldl',
                    getattr(previous, 'date', date.today() - timedelta(days=180)),
                    getattr(latest, 'date', date.today()),
                    ldl_old,
                    ldl_new
                )
                
                pdf.set_font('Helvetica', 'B', 12)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 8, f"LDL Cholesterol Analysis", 0, 1)
                
                pdf.set_font('Helvetica', '', 9)
                pdf.cell(0, 6, f"Change: {ldl_old} -> {ldl_new} mg/dL ({result.change_percent:+.1f}%)", 0, 1)
                pdf.ln(3)
                
                if result.explanation:
                    pdf.multi_cell(0, 5, result.explanation[:400])
                
                pdf.ln(5)
        
        # Generate insights from correlation engine
        insights = self.correlation_engine.generate_insights(days=30)
        
        if insights:
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(0, 51, 102)
            pdf.cell(0, 10, "Generated Insights", 0, 1)
            
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(0, 0, 0)
            
            for insight in insights[:5]:
                pdf.cell(0, 6, f"- {insight.title}", 0, 1)
    
    def _generate_use_cases(self, pdf: PDFReport):
        """Generate comprehensive use cases section."""
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 18)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 15, "Understanding Your Health Data", 0, 1)
        
        pdf.set_font('Helvetica', '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, "This section explains how you can use the Blutwerte system to "
                          "improve your health. These are practical use cases from a user's perspective.\n")
        
        # Section 1: Daily Tracking
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "1. Daily Health Tracking", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to track my daily health metrics so that I can "
                          "understand patterns and make informed decisions about my lifestyle.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "What you can track:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        tracking_items = [
            "Weight - Monitor changes over time",
            "Blood Pressure - Track systolic/diastolic readings",
            "Heart Rate - Resting and active heart rate",
            "Sleep - Hours, quality, deep sleep, REM",
            "Steps - Daily step count from your phone or watch",
            "Mood & Energy - How you feel each day",
            "Symptoms - Headaches, digestive issues, etc.",
            "Food - What you eat and drink",
            "Medications - Supplements and prescriptions",
            "Exercise - Workouts, duration, intensity"
        ]
        
        for item in tracking_items:
            pdf.cell(0, 5, f"- {item}", 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Why this matters:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, "By consistently tracking these metrics, you create a data-rich profile "
                          "that reveals correlations between your daily habits and your health outcomes. "
                          "For example, you might discover that your headaches correlate with poor sleep, "
                          "or your energy levels peak on days when you exercise.\n")
        
        # Section 2: Blood Test Understanding
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "2. Understanding Your Blood Tests", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to understand what my blood test results mean so that "
                          "I can take appropriate action to improve my health.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Key Biomarkers to Monitor:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        biomarkers = [
            ("LDL Cholesterol", "The 'bad' cholesterol - lower is better", "< 100 mg/dL"),
            ("HDL Cholesterol", "The 'good' cholesterol - higher is better", "> 60 mg/dL"),
            ("Triglycerides", "Blood fats from food - lower is better", "< 150 mg/dL"),
            ("Vitamin D", "Essential for bones and immunity", "30-60 ng/mL"),
            ("Ferritin", "Iron storage - indicates iron deficiency", "50-150 ng/mL"),
            ("Glucose", "Blood sugar - lower is better (fasting)", "70-100 mg/dL"),
            ("CRP", "Inflammation marker - lower is better", "< 1 mg/L")
        ]
        
        for name, desc, target in biomarkers:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(0, 6, f"- {name}", 0, 1)
            pdf.set_font('Helvetica', '', 9)
            pdf.cell(0, 5, f"  {desc}", 0, 1)
            pdf.cell(0, 5, f"  Target: {target}", 0, 1)
            pdf.ln(2)
        
        pdf.ln(3)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "How to Use This Data:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, "Import your blood test results into the app. The system will:\n"
                          "1. Show your current values vs. optimal ranges\n"
                          "2. Track changes over time\n"
                          "3. Suggest dietary and lifestyle changes\n"
                          "4. Identify potential causes of abnormal values\n")
        
        # Section 3: Food & Nutrition
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "3. Nutrition & Food Analysis", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to understand how my diet affects my health so that "
                          "I can make better food choices.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "How Food Affects Biomarkers:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        food_effects = [
            ("Oatmeal", "Lowers LDL cholesterol", "5-10% reduction with regular consumption"),
            ("Salmon", "Lowers triglycerides, raises HDL", "Omega-3 fatty acids are powerful"),
            ("Nuts", "Lowers LDL, raises HDL", "Plant sterols and healthy fats"),
            ("Spinach", "Provides iron and antioxidants", "Good for overall health"),
            ("Beans", "Lowers cholesterol, regulates blood sugar", "High in fiber"),
            ("Coffee", "May affect ferritin absorption", "Wait 1 hour after iron supplements")
        ]
        
        for food, effect, detail in food_effects:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(40, 6, food, 0, 0)
            pdf.set_font('Helvetica', '', 9)
            pdf.cell(0, 6, f"{effect} - {detail}", 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Practical Tips:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        tips = [
            "Pair iron-rich foods with vitamin C for better absorption",
            "Take vitamin D with a fat-containing meal",
            "Eat fatty fish (salmon, sardines) 2-3 times per week",
            "Choose whole grains over refined carbohydrates",
            "Limit processed foods high in saturated fats",
            "Stay hydrated - aim for 8 glasses of water daily"
        ]
        
        for tip in tips:
            pdf.cell(0, 5, f"- {tip}", 0, 1)
        
        # Section 4: Medication Management
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "4. Medication & Supplement Tracking", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to track my medications and supplements so that I can "
                          "maintain consistency and understand their effects on my health.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Benefits of Tracking Medications:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        med_benefits = [
            "Never miss a dose with scheduled reminders",
            "Track adherence rates over time",
            "See which supplements may be affecting your blood tests",
            "Record one-time medications (like ibuprofen for headaches)",
            "Generate reports for your doctor appointments"
        ]
        
        for benefit in med_benefits:
            pdf.cell(0, 5, f"- {benefit}", 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Common Medication Effects to Monitor:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        med_effects = [
            ("Statins", "May lower CoQ10 - consider supplementation"),
            ("Metformin", "May reduce B12 absorption"),
            ("Vitamin D", "Take with fat for best absorption"),
            ("Iron", "Take with vitamin C, avoid coffee/tea nearby"),
            ("Fish Oil", "Take with meals to reduce fishy aftertaste")
        ]
        
        for med, effect in med_effects:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(40, 6, med, 0, 0)
            pdf.set_font('Helvetica', '', 9)
            pdf.cell(0, 6, effect, 0, 1)
        
        # Section 5: Exercise & Activity
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "5. Exercise & Physical Activity", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to understand how my exercise routine affects my health "
                          "so that I can optimize my workouts.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "How Exercise Affects Biomarkers:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        exercise_effects = [
            ("Cardio (running, cycling)", "^ HDL, v triglycerides, v blood pressure"),
            ("Strength training", "^ HDL, improves insulin sensitivity"),
            ("HIIT", "^ HDL significantly, v triglycerides"),
            ("Yoga", "v cortisol (stress), may lower blood pressure"),
            ("Walking", "^ HDL gradually, improves circulation")
        ]
        
        for activity, effect in exercise_effects:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(60, 6, activity, 0, 0)
            pdf.set_font('Helvetica', '', 9)
            pdf.cell(0, 6, effect, 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Recommendations:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        recommendations = [
            "Aim for 150 minutes of moderate exercise per week",
            "Include both cardio and strength training",
            "Take rest days to allow for recovery",
            "Track heart rate during workouts",
            "Note how you feel after different types of exercise"
        ]
        
        for rec in recommendations:
            pdf.cell(0, 5, f"- {rec}", 0, 1)
        
        # Section 6: Setting Health Goals
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "6. Setting & Achieving Health Goals", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to set meaningful health goals so that I can track "
                          "my progress and stay motivated.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Types of Goals You Can Set:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        goal_types = [
            ("Biomarker Goals", "Target specific blood test values (e.g., LDL < 100)"),
            ("Weight Goals", "Lose, gain, or maintain weight"),
            ("Habit Goals", "Daily targets (10,000 steps, 8 hours sleep)"),
            ("Lifestyle Goals", "Exercise 3x per week, meditate daily")
        ]
        
        for gtype, desc in goal_types:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(50, 6, gtype, 0, 0)
            pdf.set_font('Helvetica', '', 9)
            pdf.cell(0, 6, desc, 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Tips for Success:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        success_tips = [
            "Start with one goal at a time",
            "Make goals specific and measurable",
            "Set realistic timelines (3-6 months for blood work changes)",
            "Track progress regularly",
            "Celebrate milestones along the way",
            "Adjust goals based on results"
        ]
        
        for tip in success_tips:
            pdf.cell(0, 5, f"- {tip}", 0, 1)
        
        # Section 7: Understanding Correlations
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "7. Understanding Correlations", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to understand how different aspects of my health are "
                          "connected so that I can make informed lifestyle changes.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Example Correlations:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        correlations = [
            ("Sleep -> Inflammation", "Poor sleep raises CRP (inflammation marker)"),
            ("Exercise -> HDL", "Regular cardio raises 'good' cholesterol"),
            ("Diet -> LDL", "High fiber intake lowers 'bad' cholesterol"),
            ("Stress -> Blood Pressure", "Chronic stress can raise blood pressure"),
            ("Vitamin D -> Mood", "Low vitamin D correlates with low mood"),
            ("Iron + Vitamin C", "Vitamin C dramatically improves iron absorption")
        ]
        
        for corr, explanation in correlations:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.cell(50, 5, corr[:20], 0, 0)
            pdf.set_font('Helvetica', '', 8)
            pdf.cell(0, 5, explanation[:80], 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, "The correlation engine analyzes your data to find patterns like these. "
                          "Over time, you'll see which factors most influence YOUR biomarkers.\n")
        
        # Section 8: Doctor Visits
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "8. Preparing for Doctor Visits", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "As a user, I want to make the most of my doctor appointments so that I "
                          "can get personalized advice and track progress.\n")
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "How to Prepare:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        prep_steps = [
            "Print this report to share with your doctor",
            "Note any symptoms or concerns you've tracked",
            "Bring a list of all medications and supplements",
            "Write down questions specific to your goals",
            "Ask about timing for follow-up blood tests",
            "Discuss any lifestyle changes you're considering"
        ]
        
        for step in prep_steps:
            pdf.cell(0, 5, f"- {step}", 0, 1)
        
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 7, "Questions to Ask:", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        
        questions = [
            "Are my current values cause for concern?",
            "What lifestyle changes would have the biggest impact?",
            "How often should I re-test this biomarker?",
            "Are there any interactions between my medications?",
            "Should I see a specialist for any of these values?"
        ]
        
        for q in questions:
            pdf.cell(0, 5, f"- {q}", 0, 1)
        
        # Section 9: Personal Insights
        pdf.ln(10)
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "9. Your Personal Health Journey", 0, 1)
        
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(0, 0, 0)
        
        pdf.multi_cell(0, 5, "Your health is a personal journey. The Blutwerte system helps you:\n")
        
        pdf.set_font('Helvetica', '', 10)
        
        journey_points = [
            "Track what matters to you - customize your metrics",
            "Build healthy habits through consistent tracking",
            "Connect the dots between lifestyle and health outcomes",
            "Set realistic goals based on YOUR data, not averages",
            "Stay motivated with progress tracking and milestones",
            "Make informed decisions with personalized insights"
        ]
        
        for point in journey_points:
            pdf.cell(0, 5, f"- {point}", 0, 1)
        
        pdf.ln(10)
        pdf.set_font('Helvetica', 'I', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, "Remember: Small, consistent changes lead to lasting improvements. "
                          "Your health data is a powerful tool - use it to create positive change!\n")
        
        # Closing
        pdf.ln(10)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, "About This Report", 0, 1)
        
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.cell(0, 5, f"User: {self.user_name} ({self.user_id})", 0, 1)
        pdf.cell(0, 5, "Blutwerte - Personal Health Intelligence System", 0, 1)


def generate_sample_report(filepath: str = "sample_health_report.pdf"):
    """Generate a sample report for demonstration."""
    
    from blutwerte.diary import Diary, MedicationDiary
    from blutwerte.goals import GoalManager
    from blutwerte.correlation import CorrelationEngine
    from dataclasses import dataclass
    from datetime import date, datetime, timedelta
    
    # Create mock data
    @dataclass
    class MockBloodTest:
        date: date
        ldl: float = 0
        hdl: float = 0
        triglycerides: float = 0
        ferritin: float = 0
        vitamin_d: float = 0
        glucose: float = 0
    
    blood_tests = [
        MockBloodTest(date=date(2025, 6, 1), ldl=155, hdl=45, triglycerides=150, ferritin=25, vitamin_d=20, glucose=95),
        MockBloodTest(date=date(2025, 12, 1), ldl=128, hdl=52, triglycerides=120, ferritin=35, vitamin_d=32, glucose=90),
    ]
    
    # Create diary
    diary = Diary(user_id="demo_user")
    for i in range(30):
        diary.add_entry(metric="steps", value=8000 + i*100, timestamp=datetime.now() - timedelta(days=i))
        diary.add_entry(metric="sleep_hours", value=7.5, timestamp=datetime.now() - timedelta(days=i))
    
    # Create goals
    goal_manager = GoalManager(user_id="demo_user")
    goal_manager.add_biomarker_goal("ldl", target=100, priority="high")
    goal_manager.add_biomarker_goal("vitamin_d", target=40, priority="medium")
    goal_manager.add_weight_goal(target_weight=75, current_weight=82, priority="high")
    goal_manager.add_habit_goal("steps", target=10000, priority="medium")
    
    # Update some progress
    ldl_goal = goal_manager.get_goal_by_metric("ldl")
    ldl_goal.start_value = 155
    goal_manager.update_goal_progress("ldl", 128)
    
    # Create correlation engine
    engine = CorrelationEngine(diary=diary, blood_tests=blood_tests)
    insights = engine.generate_insights(days=30)
    
    # Create medication diary
    med_diary = MedicationDiary(user_id="demo_user")
    med_diary.add_regular(name="Vitamin D", dosage=2000, unit="IU", frequency="daily")
    med_diary.add_regular(name="Fish Oil", dosage=1000, unit="mg", frequency="daily")
    
    # Generate report
    generator = HealthReportGenerator(
        user_name="Demo User",
        user_id="demo_user",
        title="Comprehensive Health Report"
    )
    
    generator.add_diary_data(diary)
    generator.add_blood_tests(blood_tests)
    generator.add_goals(goal_manager)
    generator.add_correlations(engine)
    generator.add_medication_diary(med_diary)
    generator.add_insights(insights)
    
    output_path = generator.generate_pdf(filepath)
    return output_path


__all__ = [
    'HealthReportGenerator',
    'generate_sample_report',
    'PDFReport',
]
