import streamlit as st
import altair as alt
from snowflake.snowpark.context import get_active_session

# Connect to Snowflake
session = get_active_session()

st.set_page_config(layout="wide")
st.title("AI 100 Firmographics Dashboard")
st.caption("Explore trends across valuation, geography, sectors, models, and company age.")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Funding & Valuation",
    "Geographic Trends",
    "Industry & Sectors",
    "Business Models",
    "Company Age"
])

# ---------------- TAB 1: FUNDING & VALUATION ----------------
with tab1:
    st.subheader("Top 10 Companies by Valuation")
    valuation_df = session.sql("""
        SELECT ORGNAME, VALUATION
        FROM my_firmographics
        WHERE VALUATION IS NOT NULL
        ORDER BY VALUATION DESC
        LIMIT 10
    """).to_pandas()
    
    chart1 = alt.Chart(valuation_df).mark_bar().encode(
        x=alt.X("ORGNAME:N", sort='-y'),
        y=alt.Y("VALUATION:Q"),
        tooltip=["ORGNAME", "VALUATION"]
    ).properties(width=700, height=400)

    st.altair_chart(chart1, use_container_width=True)

    st.subheader("Top 10 Countries by AI Company Count")
    country_df = session.sql("""
        SELECT COUNTRY, COUNT(*) AS company_count
        FROM my_firmographics
        WHERE COUNTRY IS NOT NULL
        GROUP BY COUNTRY
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """).to_pandas()
    country_df.columns = [col.lower().strip() for col in country_df.columns]

    chart2 = alt.Chart(country_df).mark_bar().encode(
        x=alt.X("country:N", sort='-y'),
        y=alt.Y("company_count:Q"),
        tooltip=["country", "company_count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart2, use_container_width=True)

# ---------------- TAB 2: GEOGRAPHIC TRENDS ----------------
with tab2:
    st.subheader("Top 10 Countries by Company Count")
    geo_df = session.sql("""
        SELECT COUNTRY, COUNT(*) AS company_count
        FROM my_firmographics
        WHERE COUNTRY IS NOT NULL
        GROUP BY COUNTRY
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """).to_pandas()
    geo_df.columns = [col.lower().strip() for col in geo_df.columns]

    chart_geo = alt.Chart(geo_df).mark_bar().encode(
        x=alt.X("country:N", sort='-y'),
        y=alt.Y("company_count:Q"),
        tooltip=["country", "company_count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart_geo, use_container_width=True)

# ---------------- TAB 3: INDUSTRY & SECTOR ----------------
with tab3:
    st.subheader("Top 10 Sectors")
    sector_df = session.sql("""
        SELECT SECTOR, COUNT(*) AS company_count
        FROM my_firmographics
        WHERE SECTOR IS NOT NULL
        GROUP BY SECTOR
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """).to_pandas()
    sector_df.columns = [col.lower().strip() for col in sector_df.columns]

    chart_sector = alt.Chart(sector_df).mark_bar().encode(
        x=alt.X("sector:N", sort='-y'),
        y=alt.Y("company_count:Q"),
        tooltip=["sector", "company_count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart_sector, use_container_width=True)

    st.subheader("Top 10 Industries")
    industry_df = session.sql("""
        SELECT INDUSTRY, COUNT(*) AS company_count
        FROM my_firmographics
        WHERE INDUSTRY IS NOT NULL
        GROUP BY INDUSTRY
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """).to_pandas()
    industry_df.columns = [col.lower().strip() for col in industry_df.columns]

    chart_industry = alt.Chart(industry_df).mark_bar().encode(
        x=alt.X("industry:N", sort='-y'),
        y=alt.Y("company_count:Q"),
        tooltip=["industry", "company_count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart_industry, use_container_width=True)

    st.subheader("Top 10 Sub-Industries")
    subindustry_df = session.sql("""
        SELECT SUBINDUSTRY, COUNT(*) AS company_count
        FROM my_firmographics
        WHERE SUBINDUSTRY IS NOT NULL
        GROUP BY SUBINDUSTRY
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """).to_pandas()
    subindustry_df.columns = [col.lower().strip() for col in subindustry_df.columns]

    chart_sub = alt.Chart(subindustry_df).mark_bar().encode(
        x=alt.X("subindustry:N", sort='-y'),
        y=alt.Y("company_count:Q"),
        tooltip=["subindustry", "company_count"]
    ).properties(width=700, height=400)

    st.altair_chart(chart_sub, use_container_width=True)

# ---------------- TAB 4: BUSINESS MODELS ----------------
with tab4:
    st.subheader("Top 6 Business Models by Stage")

    biz_model_df = session.sql("""
        SELECT 
            STAGE, 
            TRIM(value::string) AS BUSINESS_MODEL, 
            COUNT(*) AS COMPANY_COUNT
        FROM my_firmographics,
            LATERAL FLATTEN(INPUT => SPLIT(TO_VARCHAR(BUSINESSMODELS), ',')) 
        WHERE STAGE IS NOT NULL 
        GROUP BY STAGE, BUSINESS_MODEL
        ORDER BY BUSINESS_MODEL, COMPANY_COUNT DESC
    """).to_pandas()

    # Normalize column names
    biz_model_df.columns = [col.strip().lower() for col in biz_model_df.columns]

    # Keep only top 6 business models by total company count
    top_models = (
        biz_model_df.groupby("business_model")["company_count"]
        .sum()
        .sort_values(ascending=False)
        .head(6)
        .index.tolist()
    )

    filtered_df = biz_model_df[biz_model_df["business_model"].isin(top_models)]

    chart4 = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("stage:N", title="Startup Stage", sort="ascending"),
        y=alt.Y("company_count:Q", title="Company Count"),
        color=alt.Color("business_model:N", title="Business Model"),
        tooltip=["stage", "business_model", "company_count"]
    ).properties(height=400).interactive()

    st.altair_chart(chart4, use_container_width=True)
# ---------------- TAB 5: COMPANY AGE ----------------
with tab5:
    st.subheader("Company Age Distribution")

    age_dist_df = session.sql("""
        SELECT 
            (YEAR(CURRENT_DATE()) - FOUNDEDYEAR) AS COMPANY_AGE, 
            COUNT(*) AS COMPANY_COUNT
        FROM my_firmographics
        WHERE FOUNDEDYEAR IS NOT NULL
        GROUP BY COMPANY_AGE
        ORDER BY COMPANY_AGE
    """).to_pandas()

    age_dist_df.columns = [col.strip().lower() for col in age_dist_df.columns]

    if not age_dist_df.empty:
        chart5 = alt.Chart(age_dist_df).mark_line(point=True).encode(
            x=alt.X("company_age:Q", title="Company Age (Years)"),
            y=alt.Y("company_count:Q", title="Number of Companies"),
            tooltip=["company_age", "company_count"]
        ).properties(height=400).interactive()

        st.altair_chart(chart5, use_container_width=True)
    else:
        st.warning("No data available for Company Age distribution.")