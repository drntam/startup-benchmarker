import pandas as pd
import altair as alt
from simulator import StartupSimulator


# ---------- DARK THEME CONFIGURATION ----------

def configure_dark_theme():
    """
    Configure Altair charts with dark theme matching the website design.
    Colors: Dark backgrounds (#121212, #181818) with silver accents (#c0c0c0, #e0e0e0, #a8a8a8)
    """
    return {
        'background': '#121212',
        'title': {
            'color': '#ffffff',
            'fontSize': 18,
            'fontWeight': 600,
            'anchor': 'start'
        },
        'axis': {
            'domainColor': 'rgba(192, 192, 192, 0.2)',
            'gridColor': 'rgba(192, 192, 192, 0.1)',
            'labelColor': '#b8b8b8',
            'tickColor': 'rgba(192, 192, 192, 0.2)',
            'titleColor': '#ffffff',
            'titleFontWeight': 500
        },
        'legend': {
            'labelColor': '#b8b8b8',
            'titleColor': '#ffffff',
            'titleFontWeight': 500
        },
        'view': {
            'stroke': 'rgba(192, 192, 192, 0.2)'
        }
    }


# ---------- LINE CHART: Overall vs Industry vs Company ----------

def build_line_chart(sim: StartupSimulator):

    # overall avg
    overall = (
        sim.get_overall_average()
        .melt('year', var_name='Metric', value_name='Value')
    )
    overall['Source'] = 'Overall Average'
    overall['industry'] = ''
    overall['company'] = ''

    # industry avg
    industries = sorted(sim.df['industry'].dropna().unique())
    industry_frames = []
    for ind in industries:
        tmp = sim.get_industry_average(ind).melt(
            'year', var_name='Metric', value_name='Value'
        )
        tmp['Source'] = 'Industry Average'
        tmp['industry'] = ind
        tmp['company'] = ''
        industry_frames.append(tmp)
    industry_df = pd.concat(industry_frames, ignore_index=True)

    # ----- Company trends for all companies -----
    companies = sorted(sim.df['company'].dropna().unique())
    company_frames = []
    for comp in companies:
        cdf = sim.df[sim.df['company'] == comp]
        tmp = (
            cdf.groupby('year')[['revenue_usd', 'expenses_usd', 'profit_usd']]
            .mean()
            .reset_index()
            .melt('year', var_name='Metric', value_name='Value')
        )
        tmp['Source'] = 'Company'
        tmp['company'] = comp
        tmp['industry'] = cdf['industry'].iloc[0] if not cdf['industry'].empty else ''
        company_frames.append(tmp)
    company_df = pd.concat(company_frames, ignore_index=True)

    combined = pd.concat([overall, industry_df, company_df], ignore_index=True)

    # Clean up metric labels for facet headers
    combined['Metric'] = combined['Metric'].replace({
        'revenue_usd': 'Revenue',
        'profit_usd': 'Profit',
        'expenses_usd': 'Expenses'
    })

    # ----- Dropdown params -----
    industry_param = alt.param(
        name='industry_param',
        bind=alt.binding_select(options=industries, name='Industry: '),
        value=industries[0],
    )

    company_param = alt.param(
        name='company_param',
        bind=alt.binding_select(options=companies, name='Company: '),
        value=companies[0],
    )

    # Filter logic:
    filter_expr = (
        "(datum.Source == 'Overall Average') || "
        "(datum.Source == 'Industry Average' && datum.industry == industry_param) || "
        "(datum.Source == 'Company' && datum.company == company_param)"
    )

    # Bright colors for graphs (with dark theme)
    color_scale = alt.Scale(
        domain=['Overall Average', 'Industry Average', 'Company'],
        range=['#4FC3F7', '#66BB6A', '#FFA726']
    )

    # Base chart (width/height here, before facet)
    base = (
        alt.Chart(combined)
        .add_params(industry_param, company_param)
        .transform_filter(filter_expr)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X(
                'year:O',
                title='Year',
                axis=alt.Axis(labelAngle=0)
            ),
            y=alt.Y(
                'Value:Q',
                title='Amount (USD)',
                scale=alt.Scale(zero=False),    
                axis=alt.Axis(format='~s')         
            ),
            color=alt.Color('Source:N', scale=color_scale, title='Series'),
            tooltip=['year', 'Source', 'Metric', 'Value']
        )
        .properties(width=1500, height=400)
    )

    chart = (
        base
        .facet(row=alt.Row('Metric:N', title=None))
        .resolve_scale(y='independent')
        .properties(
            title='Startup Financial Trends: Overall vs Industry vs Company'
        )
        .configure(**configure_dark_theme())
    )

    return chart

# ---------- SCATTER: Profit Margin vs Revenue Growth ----------

def build_scatter_plot(sim: StartupSimulator):
    """
    Scatter plot: one point per company, showing
    Revenue Growth Rate vs Profit Margin, colored by industry
    with an interactive brush selection.
    """
    # Copy full dataset
    df = sim.df.copy()

    if 'profit_margin' not in df.columns:
        df['profit_margin'] = df['profit_usd'] / df['revenue_usd']

    # Sort by year so "first" and "last" make sense
    df = df.sort_values(['company', 'year'])

    # Aggregate: one row per company
    grouped = (
        df.groupby(['company', 'industry'], as_index=False)
        .agg(
            revenue_start=('revenue_usd', 'first'),
            revenue_end=('revenue_usd', 'last'),
            avg_profit_margin=('profit_margin', 'mean')
        )
    )

    # Revenue growth rate over the period
    grouped['revenue_growth_rate'] = (
        (grouped['revenue_end'] - grouped['revenue_start'])
        / grouped['revenue_start']
    )

    brush = alt.selection_interval(name='Company brush')

    # Bright colors
    industry_colors = alt.Scale(
        scheme='category20'
    )

    scatter = (
        alt.Chart(grouped)
        .mark_circle(size=60, opacity=0.7, stroke='#ffffff', strokeWidth=0.5)
        .add_params(brush)
        .encode(
            x=alt.X(
                'revenue_growth_rate:Q',
                title='Revenue Growth Rate',
                axis=alt.Axis(format='%'),
            ),
            y=alt.Y(
                'avg_profit_margin:Q',
                title='Average Profit Margin',
                axis=alt.Axis(format='%'),
            ),
            color=alt.condition(
                brush,
                alt.Color('industry:N', scale=industry_colors, legend=alt.Legend(title='Industry')),
                alt.value('#505050')  # Darker gray for unselected
            ),
            tooltip=[
                'company:N',
                'industry:N',
                alt.Tooltip('revenue_growth_rate:Q', title='Revenue Growth', format='.1%'),
                alt.Tooltip('avg_profit_margin:Q', title='Avg Profit Margin', format='.1%')
            ]
        )
        .properties(
            title='Profit Margin vs Revenue Growth by Company',
            width=1000,
            height=400
        )
        .configure(**configure_dark_theme())
    )

    return scatter

# ---------- EXPORT HELPER ----------

def export_charts(data_path='saas_financial_market_dataset.csv'):

    sim = StartupSimulator(data_path)

    line_chart = build_line_chart(sim)
    scatter = build_scatter_plot(sim)

    line_chart.save('line_chart.html')
    scatter.save('scatter_plot.html')
    print("Saved line_chart.html and scatter_plot.html")