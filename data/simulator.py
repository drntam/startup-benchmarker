# simulator.py

import pandas as pd


class StartupSimulator:
    def __init__(self, path: str):
        """
        Initialize the simulator by loading and cleaning the dataset,
        then adding derived metrics.
        """
        self.df = pd.read_csv(path)
        self.clean_data()
        self.add_derived_metrics()

    def clean_data(self):
        """
        Standardize column names and drop rows with missing values.
        """
        # lower_snake_case column names with no spaces
        self.df.columns = [c.strip().replace(' ', '_').lower() for c in self.df.columns]
        self.df.dropna(inplace=True)

    def add_derived_metrics(self):
        """
        Add derived metrics used in visualizations.
        Assumes columns: revenue_usd, expenses_usd, profit_usd.
        """
        # Profit margin (safe division)
        self.df['profit_margin'] = self.df['profit_usd'] / self.df['revenue_usd']
        self.df['profit_margin'] = self.df['profit_margin'].replace([pd.NA, pd.NaT], 0).fillna(0)

        # Simple fixed vs variable split (can be adjusted later if needed)
        self.df['fixed_cost'] = self.df['expenses_usd'] * 0.4
        self.df['variable_cost'] = self.df['expenses_usd'] * 0.6

    def get_overall_average(self) -> pd.DataFrame:
        """
        Average revenue, expenses, and profit across all companies by year.
        """
        return (
            self.df
            .groupby('year')[['revenue_usd', 'expenses_usd', 'profit_usd']]
            .mean()
            .reset_index()
        )

    def get_industry_average(self, industry: str) -> pd.DataFrame:
        """
        Average revenue, expenses, and profit within a given industry by year.
        """
        industry_df = self.df[self.df['industry'].str.lower() == industry.lower()]
        if industry_df.empty:
            raise ValueError(f"Industry '{industry}' not found in dataset.")
        return (
            industry_df
            .groupby('year')[['revenue_usd', 'expenses_usd', 'profit_usd']]
            .mean()
            .reset_index()
        )

    def get_company_trend(self, company_name: str) -> pd.DataFrame:
        """
        Time series for a single company: revenue, expenses, profit by year.
        """
        company_df = self.df[self.df['company'].str.lower() == company_name.lower()]
        if company_df.empty:
            raise ValueError(f"Company '{company_name}' not found in dataset.")
        return company_df[['year', 'revenue_usd', 'expenses_usd', 'profit_usd']]

    def get_cost_structure(self) -> pd.DataFrame:
        """
        Average fixed vs variable cost by year (for cost visualizations).
        """
        return (
            self.df
            .groupby('year')[['fixed_cost', 'variable_cost']]
            .mean()
            .reset_index()
        )