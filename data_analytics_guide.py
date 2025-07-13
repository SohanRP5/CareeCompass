import streamlit as st
import pandas as pd
import plotly.express as px

def show_analytics_documentation():
    """
    Display detailed documentation about the data analytics report
    and visualization methodologies
    """
    st.markdown("""
    <div class="card-container">
        <h2>📈 Data Analytics Report Documentation</h2>
        <p>Comprehensive guide to understanding and interpreting the analytics visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the markdown documentation file
    with open("analytics_documentation.md", "r") as f:
        documentation = f.read()
    
    # Create tabs for different sections of the documentation
    doc_sections = [
        "Visualizations Overview", 
        "Chart Interpretation", 
        "Methodology"
    ]
    
    doc_tabs = st.tabs(doc_sections)
    
    with doc_tabs[0]:  # Visualizations Overview
        st.markdown("""
        <div class="analytics-section">
            <h3>Data Visualization Overview</h3>
            <p>The Tech Career Compass analytics report includes multiple interactive visualizations 
            designed to provide deep insights into your technical skill profile.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a sample visualization gallery
        cols = st.columns(2)
        
        with cols[0]:
            # Sample heatmap
            st.markdown("### Skill Profile Heatmap")
            st.markdown("""
            A color-coded visualization of all skills grouped by domain, where darker colors 
            indicate higher proficiency levels. This provides a comprehensive overview of your 
            entire skill portfolio at a glance.
            """)
            
            # Sample data for demonstration
            domains = ["Programming", "Data & Analytics", "Infrastructure", "Soft Skills"]
            skills = ["Skill 1", "Skill 2", "Skill 3", "Skill 4"]
            
            sample_data = []
            for i, domain in enumerate(domains):
                for j, skill in enumerate(skills):
                    # Generate sample ratings that look interesting
                    if domain == "Programming":
                        rating = 4 if j < 3 else 3
                    elif domain == "Data & Analytics":
                        rating = 5 if j == 1 else 3
                    elif domain == "Infrastructure":
                        rating = 2 if j > 2 else 3
                    else:
                        rating = 4 if j % 2 == 0 else 3
                    
                    sample_data.append({"Domain": domain, "Skill": f"{skill}", "Rating": rating})
            
            df = pd.DataFrame(sample_data)
            pivot_df = df.pivot(index="Domain", columns="Skill", values="Rating")
            
            fig = px.imshow(
                pivot_df,
                color_continuous_scale="viridis",
                labels=dict(color="Rating"),
                height=300,
                aspect="auto"
            )
            fig.update_layout(margin=dict(l=40, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        with cols[1]:
            # Sample radar chart
            st.markdown("### Industry Benchmark Comparison")
            st.markdown("""
            A radar chart comparing your domain proficiency against industry benchmarks tailored 
            to your role and experience level, highlighting competitive advantages and growth areas.
            """)
            
            # Sample data for demonstration
            import plotly.graph_objects as go
            import numpy as np
            
            domains = ["Programming", "Data & Analytics", "Infrastructure", "Soft Skills"]
            your_ratings = [3.8, 4.2, 3.0, 4.5]
            benchmarks = [3.5, 3.5, 3.5, 3.5]
            
            fig = go.Figure()
            
            # Benchmark trace
            fig.add_trace(go.Scatterpolar(
                r=benchmarks + [benchmarks[0]],
                theta=domains + [domains[0]],
                fill=None,
                line=dict(color='rgba(150, 150, 150, 0.8)', width=2, dash='dash'),
                name='Industry Benchmark'
            ))
            
            # Skills trace
            fig.add_trace(go.Scatterpolar(
                r=your_ratings + [your_ratings[0]],
                theta=domains + [domains[0]],
                fill='toself',
                line=dict(color='#4a69bd', width=3),
                fillcolor='rgba(74, 105, 189, 0.3)',
                name='Your Skills'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5],
                        tickvals=[1, 2, 3, 4, 5],
                    )
                ),
                height=300,
                margin=dict(l=30, r=30, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### Additional Visualizations
        
        The comprehensive analytics report includes several other advanced visualizations:
        
        - **Domain Proficiency Comparison**: Bar chart comparing average skill levels across domains
        - **Skill Distribution by Domain**: Pie chart showing the distribution of skills across domains
        - **Skill Rating Distribution**: Histogram displaying the frequency of different skill ratings
        - **Skill Growth Trajectory**: Line chart projecting potential skill growth over time
        - **Impact-Effort Analysis**: Quadrant chart mapping skills by impact and effort to improve
        - **Skill Development Priorities**: Prioritized list of skills to focus on
        """)
    
    with doc_tabs[1]:  # Chart Interpretation
        st.markdown("""
        <div class="analytics-section">
            <h3>Chart Interpretation Guide</h3>
            <p>Detailed guidance on how to interpret each visualization to derive actionable insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### How to Interpret the Visualizations
        
        Each visualization in the analytics report is designed to highlight specific aspects 
        of your skill profile. Here's how to extract meaningful insights:
        
        #### Skill Profile Heatmap
        - **Dark clusters** indicate areas of expertise
        - **Light clusters** reveal skill gaps
        - **Pattern analysis** helps identify domain-specific strengths
        
        #### Benchmark Comparison
        - **Areas outside the benchmark** represent competitive advantages
        - **Areas inside the benchmark** highlight development opportunities
        - **Gap size** indicates priority areas for improvement
        
        #### Growth Trajectory
        - **Steeper lines** indicate faster growth potential
        - **Flatter lines** show slower progression (typical for already advanced skills)
        - **Milestone annotations** show timeframes for reaching advanced levels
        
        #### Impact-Effort Quadrants
        - **Quick Wins** (top-left): High impact with low effort - prioritize these first
        - **Major Projects** (top-right): High impact but higher effort - strategic long-term focus
        - **Fill-in Tasks** (bottom-left): Lower impact and minimal effort - address when convenient
        - **Thankless Tasks** (bottom-right): Lower impact but high effort - consider if necessary
        """)
        
        # Sample impact-effort quadrant chart for illustration
        st.markdown("### Sample Impact-Effort Quadrant Analysis")
        
        # Generate sample data
        np.random.seed(42)
        skills = ["Skill " + str(i+1) for i in range(15)]
        domains = np.random.choice(["Programming", "Data & Analytics", "Infrastructure", "Soft Skills"], 15)
        
        quadrant_data = pd.DataFrame({
            'Skill': skills,
            'Current Level': np.random.randint(1, 6, 15),
            'Domain': domains,
            'Effort': np.random.uniform(1, 9, 15),
            'Impact': np.random.uniform(1, 9, 15),
            'Goal Alignment': np.random.randint(5, 15, 15)
        })
        
        fig = px.scatter(
            quadrant_data,
            x='Effort',
            y='Impact',
            color='Domain',
            size='Goal Alignment',
            hover_name='Skill',
            color_discrete_sequence=px.colors.qualitative.Bold,
            size_max=20,
            opacity=0.8,
            height=500
        )
        
        # Add quadrant lines
        fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
        
        # Add quadrant labels
        fig.add_annotation(x=2.5, y=7.5, text="Quick Wins", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=7.5, y=7.5, text="Major Projects", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=2.5, y=2.5, text="Fill-in Tasks", showarrow=False, font=dict(size=14))
        fig.add_annotation(x=7.5, y=2.5, text="Thankless Tasks", showarrow=False, font=dict(size=14))
        
        fig.update_layout(
            xaxis=dict(
                title="Effort to Improve (Lower is Easier)",
                range=[0, 10]
            ),
            yaxis=dict(
                title="Potential Impact (Higher is Better)",
                range=[0, 10]
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        #### Key Question Framework for Analysis
        
        When reviewing your analytics report, consider these key questions:
        
        1. **Where are my clear strengths?** (Look for high ratings and areas above industry benchmarks)
        2. **Where are my most significant gaps?** (Identify skills rated 1-2 or below benchmarks)
        3. **Which skills offer the best return on learning investment?** (Focus on the Quick Wins quadrant)
        4. **Which domains show the fastest projected growth?** (Examine steeper curves in the growth projection)
        5. **How balanced is my skill profile?** (Consider the distribution across domains and levels)
        6. **What should be my learning sequence?** (Follow the prioritized skill recommendations)
        """)
    
    with doc_tabs[2]:  # Methodology
        st.markdown("""
        <div class="analytics-section">
            <h3>Analytics Methodology</h3>
            <p>Technical details about how the data is processed and analyzed to generate insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### Analytical Methods and Algorithms
        
        The Tech Career Compass analytics engine employs several advanced analytical techniques:
        
        #### Skill Mapping & Categorization
        - Skills are mapped to domains based on predefined categories and keyword analysis
        - Domains include Programming, Data & Analytics, Infrastructure, and Soft Skills
        
        #### Benchmark Generation
        Industry benchmarks are calculated based on:
        - Role-specific expectations (different for Junior vs. Senior)
        - Experience-based scaling (increases with years of experience)
        - Domain-specific industry standards
        
        #### Growth Projection Modeling
        Projections use a logarithmic growth model that accounts for:
        - Current skill level (higher levels grow slower)
        - Learning goals alignment (faster growth for aligned skills)
        - Experience-based learning rate
        - Realistic ceiling effects
        
        #### Priority Score Calculation
        The priority score for skill development is calculated using this weighted formula:
        ```
        Priority = (impact_factor * 40) +      # 40% weight to impact
                   (effort_factor * 25) +      # 25% weight to ease of acquisition
                   (alignment_factor * 20) +   # 20% weight to goal alignment
                   (level_factor * 15)         # 15% weight to current level gap
        ```
        
        This comprehensive formula ensures recommendations balance:
        - Potential value gained (impact)
        - Investment required (effort)
        - Alignment with personal goals
        - Current skill gaps
        """)
        
        # Add a mathematical formula visualization
        st.markdown("### Mathematical Models")
        
        cols = st.columns(2)
        with cols[0]:
            st.markdown("""
            #### Logarithmic Growth Model
            
            The skill growth projection uses a logarithmic model to accurately represent the 
            diminishing returns nature of skill acquisition:
            
            ```
            projected_growth = max_possible_growth * (1 - e^(-learning_rate * time))
            ```
            
            Where:
            - max_possible_growth = 5 - current_level
            - learning_rate is adjusted based on experience and goal alignment
            - time is measured in months
            """)
        
        with cols[1]:
            # Create a visual representation of logarithmic growth
            import matplotlib.pyplot as plt
            
            # Create a sample logarithmic growth curve
            x = np.linspace(0, 12, 100)
            current_level = 2
            max_growth = 5 - current_level
            learning_rate = 0.2
            y = current_level + max_growth * (1 - np.exp(-learning_rate * x))
            
            fig = px.line(
                x=x, 
                y=y, 
                labels={'x': 'Months', 'y': 'Skill Level'},
                title="Logarithmic Skill Growth Model",
                height=300
            )
            
            fig.add_hline(y=5, line_dash="dash", line_color="gray")
            fig.add_annotation(
                x=11, 
                y=4.9, 
                text="Maximum Level", 
                showarrow=False, 
                font=dict(size=10)
            )
            
            fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### Data Sources and Validation
        
        The analytics approach prioritizes data integrity and real-world applicability:
        
        - **Skill assessment data** comes directly from your self-ratings
        - **Industry benchmarks** are derived from research on technical profession expectations
        - **Growth projections** use established adult learning and skill acquisition models
        - **Priority algorithms** are based on established return-on-investment calculations
        
        All models undergo continuous validation to ensure accuracy and usefulness in real-world 
        professional development contexts.
        """)

def add_analytics_document_tab():
    """Add analytics documentation tab to the main navigation"""
    st.markdown("""
    <div class="card-container">
        <h2>📚 Documentation & Guidelines</h2>
        <p>Learn how to interpret and use the Career Compass analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("How to Use This Tool")
    st.write("""
    1. Complete the Skills Assessment
    2. Review your Analytics Dashboard
    3. Follow your Career Roadmap
    4. Update regularly to track progress
    """)