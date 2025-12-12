"""
Exploratory Data Analysis (EDA) - Complete Implementation
Author: [Your Name]
Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class EDAAnalyzer:
    """
    A comprehensive class for performing Exploratory Data Analysis
    """
    
    def __init__(self, filepath):
        """Initialize with dataset filepath"""
        self.filepath = filepath
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load dataset from file"""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            elif self.filepath.endswith('.xlsx'):
                self.df = pd.read_excel(self.filepath)
            else:
                raise ValueError("Unsupported file format. Use CSV or XLSX.")
            print(f"✓ Data loaded successfully: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        except Exception as e:
            print(f"✗ Error loading data: {e}")
    
    def ask_meaningful_questions(self):
        """
        Step 1: Ask meaningful questions about the dataset
        """
        print("\n" + "="*80)
        print("STEP 1: MEANINGFUL QUESTIONS ABOUT THE DATASET")
        print("="*80)
        
        questions = [
            "1. What is the overall structure and size of the dataset?",
            "2. What types of variables do we have (numerical, categorical)?",
            "3. Are there any missing values, and how should we handle them?",
            "4. What are the distributions of key variables?",
            "5. Are there any outliers that need investigation?",
            "6. What relationships exist between variables?",
            "7. Are there any temporal patterns (if time data exists)?",
            "8. What insights can we derive for business/research decisions?"
        ]
        
        for q in questions:
            print(f"  {q}")
        print()
    
    def explore_data_structure(self):
        """
        Step 2: Explore data structure, variables, and data types
        """
        print("\n" + "="*80)
        print("STEP 2: DATA STRUCTURE EXPLORATION")
        print("="*80)
        
        print("\n📊 Dataset Shape:")
        print(f"   Rows: {self.df.shape[0]:,}")
        print(f"   Columns: {self.df.shape[1]}")
        
        print("\n📋 Column Information:")
        print(self.df.info())
        
        print("\n📈 Data Types Summary:")
        print(self.df.dtypes.value_counts())
        
        print("\n🔍 First 5 Rows:")
        print(self.df.head())
        
        print("\n🔍 Last 5 Rows:")
        print(self.df.tail())
        
        print("\n📊 Statistical Summary (Numerical Columns):")
        print(self.df.describe())
        
        # Identify column types
        self.numerical_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"\n✓ Numerical Columns ({len(self.numerical_cols)}): {self.numerical_cols}")
        print(f"✓ Categorical Columns ({len(self.categorical_cols)}): {self.categorical_cols}")
    
    def identify_data_quality_issues(self):
        """
        Step 5 (moved up): Detect potential data issues
        """
        print("\n" + "="*80)
        print("STEP 3: DATA QUALITY ASSESSMENT")
        print("="*80)
        
        # Missing values
        print("\n🔍 Missing Values Analysis:")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Missing_Count': missing,
            'Missing_Percentage': missing_pct
        })
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
        
        if len(missing_df) > 0:
            print(missing_df)
            
            # Visualize missing values
            plt.figure(figsize=(10, 6))
            missing_df['Missing_Percentage'].plot(kind='barh', color='coral')
            plt.xlabel('Missing Percentage (%)')
            plt.title('Missing Values by Column')
            plt.tight_layout()
            plt.savefig('missing_values.png', dpi=300, bbox_inches='tight')
            print("   ✓ Missing values plot saved: missing_values.png")
            plt.close()
        else:
            print("   ✓ No missing values found!")
        
        # Duplicate rows
        print("\n🔍 Duplicate Rows:")
        duplicates = self.df.duplicated().sum()
        print(f"   Total duplicates: {duplicates} ({(duplicates/len(self.df)*100):.2f}%)")
        
        # Data type issues
        print("\n🔍 Potential Data Type Issues:")
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    pd.to_numeric(self.df[col])
                    print(f"   ⚠ '{col}' is stored as object but could be numeric")
                except:
                    pass
    
    def identify_patterns_and_trends(self):
        """
        Step 3: Identify trends, patterns, and anomalies
        """
        print("\n" + "="*80)
        print("STEP 4: PATTERNS, TRENDS, AND ANOMALIES")
        print("="*80)
        
        # Distribution analysis for numerical columns
        if len(self.numerical_cols) > 0:
            print("\n📊 Distribution Analysis (Numerical Variables):")
            
            n_cols = min(3, len(self.numerical_cols))
            n_rows = (len(self.numerical_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
            axes = axes.flatten() if n_rows > 1 else [axes]
            
            for idx, col in enumerate(self.numerical_cols):
                axes[idx].hist(self.df[col].dropna(), bins=30, color='skyblue', edgecolor='black')
                axes[idx].set_title(f'Distribution of {col}')
                axes[idx].set_xlabel(col)
                axes[idx].set_ylabel('Frequency')
                
                # Add statistics
                mean_val = self.df[col].mean()
                median_val = self.df[col].median()
                axes[idx].axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
                axes[idx].axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val:.2f}')
                axes[idx].legend()
            
            # Hide extra subplots
            for idx in range(len(self.numerical_cols), len(axes)):
                axes[idx].axis('off')
            
            plt.tight_layout()
            plt.savefig('distributions.png', dpi=300, bbox_inches='tight')
            print("   ✓ Distribution plots saved: distributions.png")
            plt.close()
        
        # Outlier detection using IQR method
        print("\n🔍 Outlier Detection (IQR Method):")
        outlier_summary = {}
        
        for col in self.numerical_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col]
            outlier_summary[col] = len(outliers)
            
            if len(outliers) > 0:
                print(f"   {col}: {len(outliers)} outliers ({len(outliers)/len(self.df)*100:.2f}%)")
        
        # Box plots for outlier visualization
        if len(self.numerical_cols) > 0:
            fig, axes = plt.subplots(1, min(4, len(self.numerical_cols)), figsize=(15, 5))
            if len(self.numerical_cols) == 1:
                axes = [axes]
            
            for idx, col in enumerate(self.numerical_cols[:4]):
                self.df.boxplot(column=col, ax=axes[idx])
                axes[idx].set_title(f'{col}')
                axes[idx].set_ylabel('Value')
            
            plt.tight_layout()
            plt.savefig('boxplots_outliers.png', dpi=300, bbox_inches='tight')
            print("   ✓ Boxplot saved: boxplots_outliers.png")
            plt.close()
        
        # Categorical variable analysis
        if len(self.categorical_cols) > 0:
            print("\n📊 Categorical Variables Analysis:")
            for col in self.categorical_cols[:5]:  # First 5 categorical columns
                print(f"\n   {col}:")
                value_counts = self.df[col].value_counts()
                print(f"      Unique values: {len(value_counts)}")
                print(f"      Most common: {value_counts.index[0]} ({value_counts.iloc[0]} occurrences)")
    
    def test_hypotheses(self):
        """
        Step 4: Test hypotheses and validate assumptions
        """
        print("\n" + "="*80)
        print("STEP 5: HYPOTHESIS TESTING & VALIDATION")
        print("="*80)
        
        # Normality tests for numerical columns
        print("\n📊 Normality Tests (Shapiro-Wilk):")
        for col in self.numerical_cols[:5]:  # Test first 5 numerical columns
            sample = self.df[col].dropna().sample(min(5000, len(self.df[col].dropna())))
            stat, p_value = stats.shapiro(sample)
            is_normal = "Yes" if p_value > 0.05 else "No"
            print(f"   {col}: p-value = {p_value:.4f} | Normal distribution? {is_normal}")
        
        # Correlation analysis
        if len(self.numerical_cols) > 1:
            print("\n📊 Correlation Analysis:")
            corr_matrix = self.df[self.numerical_cols].corr()
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                       fmt='.2f', square=True, linewidths=1)
            plt.title('Correlation Matrix')
            plt.tight_layout()
            plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
            print("   ✓ Correlation matrix saved: correlation_matrix.png")
            plt.close()
            
            # Find strong correlations
            print("\n   Strong Correlations (|r| > 0.7):")
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        strong_corr.append((corr_matrix.columns[i], 
                                          corr_matrix.columns[j], 
                                          corr_matrix.iloc[i, j]))
            
            if strong_corr:
                for col1, col2, corr_val in strong_corr:
                    print(f"      {col1} <-> {col2}: {corr_val:.3f}")
            else:
                print("      No strong correlations found")
        
        # Chi-square test for categorical variables
        if len(self.categorical_cols) >= 2:
            print("\n📊 Chi-Square Test (Categorical Independence):")
            cat1, cat2 = self.categorical_cols[0], self.categorical_cols[1]
            contingency_table = pd.crosstab(self.df[cat1], self.df[cat2])
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
            print(f"   {cat1} vs {cat2}:")
            print(f"      Chi-square statistic: {chi2:.4f}")
            print(f"      p-value: {p_value:.4f}")
            print(f"      Independent? {'No' if p_value < 0.05 else 'Yes'}")
    
    def generate_insights_report(self):
        """
        Generate a comprehensive insights report
        """
        print("\n" + "="*80)
        print("STEP 6: KEY INSIGHTS & RECOMMENDATIONS")
        print("="*80)
        
        insights = []
        
        # Dataset overview
        insights.append(f"✓ Dataset contains {self.df.shape[0]:,} records and {self.df.shape[1]} features")
        
        # Missing data insight
        missing_pct = (self.df.isnull().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100
        if missing_pct > 5:
            insights.append(f"⚠ {missing_pct:.2f}% of data is missing - consider imputation strategies")
        elif missing_pct > 0:
            insights.append(f"✓ Only {missing_pct:.2f}% of data is missing - minimal impact expected")
        else:
            insights.append("✓ No missing values detected - clean dataset")
        
        # Outlier insight
        outlier_cols = []
        for col in self.numerical_cols:
            Q1, Q3 = self.df[col].quantile(0.25), self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[col] < Q1 - 1.5*IQR) | (self.df[col] > Q3 + 1.5*IQR)]
            if len(outliers) > len(self.df) * 0.05:
                outlier_cols.append(col)
        
        if outlier_cols:
            insights.append(f"⚠ Significant outliers detected in: {', '.join(outlier_cols)}")
        
        # Distribution insight
        skewed_cols = []
        for col in self.numerical_cols:
            skewness = self.df[col].skew()
            if abs(skewness) > 1:
                skewed_cols.append(f"{col} (skew: {skewness:.2f})")
        
        if skewed_cols:
            insights.append(f"⚠ Highly skewed distributions: {', '.join(skewed_cols)}")
        
        print("\n📋 Key Insights:")
        for idx, insight in enumerate(insights, 1):
            print(f"   {idx}. {insight}")
        
        print("\n💡 Recommendations:")
        recommendations = [
            "1. Handle missing values using appropriate imputation methods",
            "2. Consider transformation for skewed variables (log, sqrt, box-cox)",
            "3. Investigate and handle outliers based on domain knowledge",
            "4. Feature engineering based on correlation insights",
            "5. Consider dimensionality reduction if high correlation exists"
        ]
        for rec in recommendations:
            print(f"   {rec}")
    
    def run_complete_eda(self):
        """
        Run the complete EDA pipeline
        """
        print("\n" + "="*80)
        print("EXPLORATORY DATA ANALYSIS - COMPLETE PIPELINE")
        print("="*80)
        
        self.ask_meaningful_questions()
        self.explore_data_structure()
        self.identify_data_quality_issues()
        self.identify_patterns_and_trends()
        self.test_hypotheses()
        self.generate_insights_report()
        
        print("\n" + "="*80)
        print("EDA COMPLETE! All visualizations saved.")
        print("="*80)


# Example usage
if __name__ == "__main__":
    # Replace with your dataset path
    dataset_path = "your_dataset.csv"
    
    # Create EDA analyzer
    eda = EDAAnalyzer(dataset_path)
    
    # Run complete analysis
    eda.run_complete_eda()
    
    # You can also run individual steps:
    # eda.ask_meaningful_questions()
    # eda.explore_data_structure()
    # etc.
