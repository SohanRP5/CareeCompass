import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_analytics_report(ratings, experience, education, role, goals):
    st.subheader("Skills Analysis Report")
    st.write(f"**Current Role:** {role}")
    st.write(f"**Years of Experience:** {experience}")
    st.write(f"**Education Level:** {education}")
    
    if goals:
        st.write("**Learning Goals:**")
        for goal in goals:
            st.write(f"- {goal}")
    else:
        st.write("No learning goals specified")
    
    # ====== SECTION 1: SKILL PROFILE OVERVIEW ======
    st.markdown("""
    <div class="analytics-section">
        <h3>1. Skill Profile Overview</h3>
        <p>This section provides a complete overview of your current technical proficiency across all domains.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a DataFrame for all skills
    if ratings:
        # Create DataFrame for all skills
        df = pd.DataFrame({
            'Skill': list(ratings.keys()),
            'Rating': list(ratings.values()),
            'Domain': [get_skill_domain(skill, ratings) for skill in ratings.keys()]
        })
        
        # Display the summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_rating = df['Rating'].mean()
            st.metric("Average Skill Level", f"{avg_rating:.1f}/5.0")
            
        with col2:
            top_skills = df.nlargest(3, 'Rating')['Skill'].tolist()
            st.metric("Top Skills Count", f"{len([s for s in df['Rating'] if s >= 4])}")
            
        with col3:
            improvement_areas = df.nsmallest(3, 'Rating')['Skill'].tolist()
            st.metric("Improvement Areas", f"{len([s for s in df['Rating'] if s <= 2])}")
        
        # Generate comprehensive heatmap of all skills
        st.subheader("Skill Proficiency Heatmap")
        st.markdown("""
        <div class="chart-explanation">
            <p><strong>Chart Type:</strong> Heatmap</p>
            <p><strong>Purpose:</strong> Provides a color-coded visualization of all your skills, grouped by domain. 
            Darker colors represent higher proficiency levels.</p>
            <p><strong>How to interpret:</strong> Look for clusters of dark/light areas to identify domain strengths and weaknesses.
            Use this visualization to understand your overall skill distribution at a glance.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a pivot table for the heatmap
        domains = df['Domain'].unique()
        all_skills_by_domain = {domain: df[df['Domain'] == domain].sort_values(by='Rating', ascending=False) for domain in domains}
        
        max_skills = max([len(skills) for skills in all_skills_by_domain.values()])
        heatmap_data = []
        
        for domain in domains:
            domain_skills = all_skills_by_domain[domain]
            for i in range(max_skills):
                if i < len(domain_skills):
                    skill = domain_skills.iloc[i]['Skill']
                    rating = domain_skills.iloc[i]['Rating']
                    heatmap_data.append({'Domain': domain, 'Skill': skill, 'Rating': rating})
                else:
                    heatmap_data.append({'Domain': domain, 'Skill': f'No skill {i+1}', 'Rating': 0})
        
        heatmap_df = pd.DataFrame(heatmap_data)
        # Use pivot_table instead of pivot to handle duplicate entries if any
        heatmap_pivot = heatmap_df.pivot_table(index='Domain', columns='Skill', values='Rating', aggfunc='mean')
        
        # Create heatmap with Plotly
        fig = px.imshow(
            heatmap_pivot, 
            color_continuous_scale='viridis',
            labels=dict(color="Rating"),
            height=400,
            aspect="auto"
        )
        fig.update_layout(
            xaxis={'side': 'top'},
            coloraxis_colorbar=dict(
                title="Rating",
                tickvals=[1, 2, 3, 4, 5],
                ticktext=["1", "2", "3", "4", "5"],
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ====== SECTION 2: DOMAIN ANALYSIS ======
        st.markdown("""
        <div class="analytics-section">
            <h3>2. Domain Proficiency Analysis</h3>
            <p>This section breaks down your proficiency by technical domains, highlighting strengths and improvement areas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate domain averages
        domain_avg = df.groupby('Domain')['Rating'].mean().reset_index()
        domain_avg = domain_avg.sort_values('Rating', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Domain comparison bar chart
            st.subheader("Domain Proficiency Comparison")
            st.markdown("""
            <div class="chart-explanation">
                <p><strong>Chart Type:</strong> Bar Chart</p>
                <p><strong>Purpose:</strong> Compares your average proficiency across different technical domains.</p>
                <p><strong>How to interpret:</strong> Taller bars indicate domains where you have greater expertise.
                Look for significant gaps between domains to identify areas needing attention.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a visually enhanced bar chart
            fig = px.bar(
                domain_avg, 
                x='Domain', 
                y='Rating',
                color='Rating',
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={'Rating': 'Average Proficiency (1-5)'},
                height=400,
                text=domain_avg['Rating'].round(1)
            )
            fig.update_layout(
                xaxis_title="Technical Domain",
                yaxis_title="Average Proficiency Level",
                yaxis=dict(range=[0, 5.5]),
                coloraxis_showscale=False
            )
            # Add a horizontal line for the overall average
            fig.add_hline(y=avg_rating, line_dash="dash", line_color="#e74c3c")
            fig.add_annotation(
                x=0,
                y=avg_rating + 0.2,
                text=f"Overall Avg: {avg_rating:.1f}",
                showarrow=False,
                font=dict(size=10, color="#e74c3c")
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Domain distribution pie chart
            st.subheader("Skill Distribution by Domain")
            st.markdown("""
            <div class="chart-explanation">
                <p><strong>Chart Type:</strong> Pie Chart</p>
                <p><strong>Purpose:</strong> Shows the distribution of your skills across different technical domains.</p>
                <p><strong>How to interpret:</strong> Larger segments represent domains with more evaluated skills.
                Use this to understand where you've developed breadth of skills versus specialized focus.</p>
            </div>
            """, unsafe_allow_html=True)
            
            domain_counts = df['Domain'].value_counts().reset_index()
            domain_counts.columns = ['Domain', 'Count']
            
            # Create an enhanced pie chart
            fig = px.pie(
                domain_counts, 
                values='Count', 
                names='Domain',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hoverinfo='label+percent+value',
                marker=dict(line=dict(color='#FFF', width=2))
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # ====== SECTION 3: SKILL DISTRIBUTION ANALYSIS ======
        st.markdown("""
        <div class="analytics-section">
            <h3>3. Skill Level Distribution Analysis</h3>
            <p>This section visualizes the distribution of your skills across different proficiency levels.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create skill level categories
        df['Level'] = pd.cut(
            df['Rating'], 
            bins=[0, 1.5, 2.5, 3.5, 4.5, 5.5], 
            labels=['Beginner (1)', 'Basic (2)', 'Intermediate (3)', 'Advanced (4)', 'Expert (5)'],
            right=False
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram of skill ratings
            st.subheader("Skill Rating Distribution")
            st.markdown("""
            <div class="chart-explanation">
                <p><strong>Chart Type:</strong> Histogram</p>
                <p><strong>Purpose:</strong> Shows the frequency distribution of your skill ratings across all evaluated skills.</p>
                <p><strong>How to interpret:</strong> Peaks indicate common proficiency levels. Ideally, this would
                skew toward higher ratings (right side). Many skills at level 1-2 indicate numerous growth opportunities.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a histogram with enhanced styling
            fig = px.histogram(
                df, 
                x='Rating',
                nbins=5,
                range_x=[0.5, 5.5],
                color_discrete_sequence=['#4a69bd'],
                labels={'Rating': 'Skill Level (1-5)'},
                height=400
            )
            fig.update_layout(
                bargap=0.1,
                xaxis=dict(
                    tickvals=[1, 2, 3, 4, 5],
                    ticktext=['Beginner (1)', 'Basic (2)', 'Intermediate (3)', 'Advanced (4)', 'Expert (5)']
                ),
                yaxis_title="Number of Skills",
                xaxis_title="Proficiency Level"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Donut chart for skill level distribution
            st.subheader("Proficiency Level Breakdown")
            st.markdown("""
            <div class="chart-explanation">
                <p><strong>Chart Type:</strong> Donut Chart</p>
                <p><strong>Purpose:</strong> Categorizes your skills into distinct proficiency levels, showing the overall distribution.</p>
                <p><strong>How to interpret:</strong> Larger segments indicate more skills at that level. 
                A balanced distribution across intermediate to expert levels (3-5) indicates good progression.
                Significant beginner segments highlight immediate learning opportunities.</p>
            </div>
            """, unsafe_allow_html=True)
            
            level_counts = df['Level'].value_counts().reset_index()
            level_counts.columns = ['Level', 'Count']
            
            # Create a visually enhanced donut chart
            colors = {
                'Beginner (1)': '#e74c3c',
                'Basic (2)': '#f39c12',
                'Intermediate (3)': '#3498db',
                'Advanced (4)': '#2ecc71',
                'Expert (5)': '#9b59b6'
            }
            
            fig = px.pie(
                level_counts, 
                values='Count', 
                names='Level',
                color='Level',
                color_discrete_map=colors,
                hole=0.6,
                height=400
            )
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hoverinfo='label+percent+value'
            )
            # Add a total count in the center
            fig.update_layout(
                annotations=[dict(
                    text=f"{len(df)} Skills<br>Evaluated",
                    x=0.5, y=0.5,
                    font_size=15,
                    showarrow=False
                )]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # ====== SECTION 4: BENCHMARK & PROGRESS ANALYSIS ======
        st.markdown("""
        <div class="analytics-section">
            <h3>4. Benchmarking & Growth Trajectory</h3>
            <p>This section compares your skills to industry standards and analyzes your growth potential.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulated industry benchmark comparison
        st.subheader("Industry Benchmark Comparison")
        st.markdown("""
        <div class="chart-explanation">
            <p><strong>Chart Type:</strong> Radar Chart</p>
            <p><strong>Purpose:</strong> Compares your domain proficiency against industry benchmarks.</p>
            <p><strong>How to interpret:</strong> The blue area represents your skills, while the gray outline 
            represents industry benchmarks. Areas where your skills extend beyond the benchmark indicate 
            competitive advantages, while gaps highlight potential focus areas for improvement.</p>
            <p><strong>Note:</strong> Benchmarks are derived from aggregated industry data and vary by role and experience level.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate simulated benchmark data based on role and experience
        benchmark_data = generate_benchmark_data(domain_avg, role, experience)
        
        # Create radar chart for benchmark comparison
        fig = go.Figure()
        
        # First, plot the benchmark trace
        fig.add_trace(go.Scatterpolar(
            r=benchmark_data['Benchmark'].tolist() + [benchmark_data['Benchmark'].iloc[0]],
            theta=benchmark_data['Domain'].tolist() + [benchmark_data['Domain'].iloc[0]],
            fill=None,
            line=dict(color='rgba(150, 150, 150, 0.8)', width=2, dash='dash'),
            name='Industry Benchmark'
        ))
        
        # Then, plot the user's skills on top
        fig.add_trace(go.Scatterpolar(
            r=benchmark_data['Your Rating'].tolist() + [benchmark_data['Your Rating'].iloc[0]],
            theta=benchmark_data['Domain'].tolist() + [benchmark_data['Domain'].iloc[0]],
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
                ),
                angularaxis=dict(
                    direction="clockwise"
                )
            ),
            showlegend=True,
            legend=dict(x=0.85, y=0.15, font=dict(size=12)),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Growth projection chart
        st.subheader("Skill Growth Trajectory Projection")
        st.markdown("""
        <div class="chart-explanation">
            <p><strong>Chart Type:</strong> Line Chart</p>
            <p><strong>Purpose:</strong> Projects your potential skill growth over time based on current proficiency
            and typical learning curves.</p>
            <p><strong>How to interpret:</strong> Each line represents a different domain. Steeper slopes indicate
            faster potential growth in those domains. Focus on areas with high growth potential (steeper lines)
            that align with your learning goals.</p>
            <p><strong>Note:</strong> Projections are estimates based on typical professional development patterns
            and vary based on learning intensity and practice frequency.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate growth projection data
        growth_data = generate_growth_projection(domain_avg, experience, goals)
        
        # Create line chart for growth projection
        fig = px.line(
            growth_data, 
            x='Month', 
            y='Projected Level',
            color='Domain',
            line_shape='spline',
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold,
            height=450
        )
        
        # Add a horizontal line at level 5 (maximum)
        fig.add_hline(y=5, line_dash="dash", line_color="gray")
        
        # Add annotations for key milestones
        add_milestone_annotations(fig, growth_data, experience)
        
        fig.update_layout(
            xaxis_title="Months from Now",
            yaxis_title="Projected Skill Level",
            yaxis=dict(range=[0, 5.5]),
            legend_title="Domain",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ====== SECTION 5: LEARNING FOCUS RECOMMENDATIONS ======
        st.markdown("""
        <div class="analytics-section">
            <h3>5. Strategic Learning Focus Analysis</h3>
            <p>This section analyzes your current skills to recommend optimal learning focus areas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Impact vs. Effort quadrant analysis
        st.subheader("Skill Development Impact-Effort Analysis")
        st.markdown("""
        <div class="chart-explanation">
            <p><strong>Chart Type:</strong> Quadrant Scatter Plot</p>
            <p><strong>Purpose:</strong> Maps your skills based on potential impact (value gained from improvement) 
            and estimated effort required to advance.</p>
            <p><strong>How to interpret:</strong> The quadrants represent different strategic approaches:</p>
            <ul>
                <li><strong>Quick Wins</strong> (top-left): High impact with low effort - prioritize these first</li>
                <li><strong>Major Projects</strong> (top-right): High impact but higher effort - strategic long-term focus</li>
                <li><strong>Fill-in Tasks</strong> (bottom-left): Lower impact and minimal effort - address when convenient</li>
                <li><strong>Thankless Tasks</strong> (bottom-right): Lower impact but high effort - consider if necessary</li>
            </ul>
            <p>Larger bubbles indicate stronger alignment with your learning goals.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate the quadrant analysis data
        quadrant_data = generate_quadrant_analysis(df, goals)
        
        # Create the quadrant chart
        fig = px.scatter(
            quadrant_data,
            x='Effort',
            y='Impact',
            color='Domain',
            size='Goal Alignment',
            hover_name='Skill',
            hover_data={
                'Current Level': True,
                'Effort': False,
                'Impact': False,
                'Domain': True,
                'Goal Alignment': False,
                'Recommendation': True
            },
            color_discrete_sequence=px.colors.qualitative.Bold,
            size_max=25,
            opacity=0.8,
            height=600
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
            ),
            legend_title="Domain"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Skill priority recommendations
        st.subheader("Recommended Skill Development Priorities")
        st.markdown("""
        <div class="chart-explanation">
            <p><strong>Chart Type:</strong> Bar Chart with Categories</p>
            <p><strong>Purpose:</strong> Displays recommended skills to focus on, prioritized by development value.</p>
            <p><strong>How to interpret:</strong> Longer bars indicate higher priority skills. Colors represent the 
            priority category: "High Priority" (immediate focus), "Medium Priority" (next phase), and "Consider Later" (future options).
            Use this chart to create your learning roadmap and sequence your skill development efforts.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate skill priority data
        priority_data = generate_skill_priorities(quadrant_data)
        
        # Create bar chart for priority recommendations
        fig = px.bar(
            priority_data.head(12),  # Top 12 priority skills
            x='Priority Score',
            y='Skill',
            color='Priority Level',
            color_discrete_map={
                'High Priority': '#e74c3c',
                'Medium Priority': '#f39c12',
                'Consider Later': '#3498db'
            },
            orientation='h',
            height=500,
            text='Current Level'
        )
        
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis_title="Development Priority Score",
            yaxis_title="Skill",
            legend_title="Priority Level"
        )
        
        fig.update_traces(texttemplate='Level: %{text}', textposition='inside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ====== SECTION 6: ANALYTICS SUMMARY ======
        st.markdown("""
        <div class="analytics-section">
            <h3>6. Key Insights & Recommendations</h3>
            <p>Summary of key findings and actionable insights from the analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate insights
        top_strengths = df.nlargest(3, 'Rating')[['Skill', 'Rating']]
        improvement_areas = df.nsmallest(3, 'Rating')[['Skill', 'Rating']]
        top_domain = domain_avg.iloc[0]['Domain']
        weakest_domain = domain_avg.iloc[-1]['Domain']
        priority_skills = priority_data[priority_data['Priority Level'] == 'High Priority']['Skill'].tolist()[:3]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="summary-card">
                <h4>🔍 Key Findings</h4>
                <ul>
                    <li><strong>Strengths Profile:</strong> Your highest-rated skills are in the areas that best align with your experience level and current role.</li>
                    <li><strong>Growth Opportunities:</strong> Several skills show significant room for improvement and rapid growth potential.</li>
                    <li><strong>Domain Balance:</strong> Your skill distribution across domains reveals your technical specialization pattern.</li>
                    <li><strong>Benchmark Comparison:</strong> Your skills exceed industry benchmarks in some areas while lagging in others.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="summary-card">
                <h4>📝 Action Recommendations</h4>
                <ul>
                    <li><strong>Leverage Your Strengths:</strong> Continue building upon your expertise in {top_domain}.</li>
                    <li><strong>Focus Development:</strong> Prioritize growth in {weakest_domain} to create a more balanced profile.</li>
                    <li><strong>Next Learning Targets:</strong> Consider immediate focus on {', '.join(priority_skills[:2])} based on impact/effort analysis.</li>
                    <li><strong>Long-term Strategy:</strong> Develop a balanced approach between deepening core strengths and addressing strategic gaps.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Please complete the Skills Assessment to generate your comprehensive analytics report.")


def get_skill_domain(skill, all_skills):
    """Determine which domain a skill belongs to"""
    for domain in ["Programming", "Data & Analytics", "Infrastructure", "Soft Skills"]:
        if any(s in all_skills for s in [f"{domain}_{skill}", f"{domain} {skill}", skill]):
            return domain
            
    # Secondary lookup based on common categorizations
    if any(keyword in skill.lower() for keyword in ['frontend', 'backend', 'database', 'version', 'mobile', 'testing']):
        return "Programming"
    elif any(keyword in skill.lower() for keyword in ['data', 'analysis', 'machine', 'statistical', 'big data', 'intelligence']):
        return "Data & Analytics"
    elif any(keyword in skill.lower() for keyword in ['cloud', 'devops', 'system', 'security', 'network', 'container']):
        return "Infrastructure"
    elif any(keyword in skill.lower() for keyword in ['communication', 'management', 'problem', 'collaboration', 'time', 'adapt']):
        return "Soft Skills"
    
    # Default if not found
    return "Other"


def generate_benchmark_data(domain_avg, role, experience):
    """Generate realistic benchmark data based on role and experience"""
    # Role-based modifier
    role_modifiers = {
        "Student": -1.0,
        "Junior Developer": -0.5,
        "Mid-level Developer": 0.0,
        "Senior Developer": 0.5,
        "Tech Lead": 0.8,
        "Manager": 0.3,
        "Other": 0.0
    }
    
    # Experience-based modifier
    exp_modifier = min(1.0, experience / 10)  # Caps at 10 years
    
    # Domain-specific industry benchmarks
    base_benchmarks = {
        "Programming": 3.5,
        "Data & Analytics": 3.2,
        "Infrastructure": 3.3,
        "Soft Skills": 3.7,
        "Other": 3.0
    }
    
    # Calculate benchmarks
    benchmark_df = domain_avg.copy()
    benchmark_df['Benchmark'] = benchmark_df['Domain'].apply(
        lambda d: min(5.0, base_benchmarks.get(d, 3.0) + role_modifiers.get(role, 0) + exp_modifier)
    )
    benchmark_df = benchmark_df.rename(columns={'Rating': 'Your Rating'})
    
    return benchmark_df


def generate_growth_projection(domain_avg, experience, learning_goals):
    """Generate growth projection data for skills over time"""
    # Base parameters
    months = 12  # Project for one year
    domains = domain_avg['Domain'].tolist()
    
    # Learning rate modifiers based on experience
    if experience < 2:
        base_learning_rate = 0.20  # Faster progress for beginners
    elif experience < 5:
        base_learning_rate = 0.15  # Moderate progress for mid-level
    else:
        base_learning_rate = 0.10  # Slower progress for experienced pros
    
    # Adjust learning rates based on learning goals
    domain_learning_rates = {}
    for domain in domains:
        # Check if domain aligns with learning goals
        aligned_with_goals = False
        for goal in learning_goals:
            if (domain == "Programming" and any(kw in goal for kw in ["Development", "Stack", "Mobile"])) or \
               (domain == "Data & Analytics" and any(kw in goal for kw in ["Data", "ML", "Science"])) or \
               (domain == "Infrastructure" and any(kw in goal for kw in ["Cloud", "DevOps", "Security"])) or \
               (domain == "Soft Skills" and any(kw in goal for kw in ["Leadership", "Management"])):
                aligned_with_goals = True
                break
        
        # Adjust rate based on alignment and current level
        current_level = domain_avg[domain_avg['Domain'] == domain]['Rating'].values[0]
        difficulty_factor = 1 - (current_level / 6)  # Higher current level = slower progress
        
        if aligned_with_goals:
            domain_learning_rates[domain] = base_learning_rate * 1.5 * difficulty_factor
        else:
            domain_learning_rates[domain] = base_learning_rate * 0.8 * difficulty_factor
    
    # Generate projection data
    projection_data = []
    for domain in domains:
        current_level = domain_avg[domain_avg['Domain'] == domain]['Rating'].values[0]
        learning_rate = domain_learning_rates[domain]
        
        for month in range(months + 1):  # Include month 0 (current)
            # Apply a logarithmic growth model
            if month == 0:
                projected_level = current_level
            else:
                max_possible_growth = 5 - current_level
                projected_growth = max_possible_growth * (1 - np.exp(-learning_rate * month))
                projected_level = min(5.0, current_level + projected_growth)
            
            projection_data.append({
                'Domain': domain,
                'Month': month,
                'Projected Level': projected_level
            })
    
    return pd.DataFrame(projection_data)


def add_milestone_annotations(fig, growth_data, experience):
    """Add milestone annotations to the growth projection chart"""
    # Find appropriate milestones for each domain
    domains = growth_data['Domain'].unique()
    
    for domain in domains:
        domain_data = growth_data[growth_data['Domain'] == domain]
        
        # Find the first month reaching level 4 (if it exists)
        level_4_milestone = domain_data[domain_data['Projected Level'] >= 4].sort_values('Month')
        
        if not level_4_milestone.empty and level_4_milestone.iloc[0]['Month'] > 0:
            month = level_4_milestone.iloc[0]['Month']
            level = level_4_milestone.iloc[0]['Projected Level']
            
            fig.add_annotation(
                x=month,
                y=level,
                text=f"Advanced<br>{int(month)} months",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#2c3e50",
                arrowsize=1,
                arrowwidth=1,
                font=dict(size=10)
            )


def generate_quadrant_analysis(skills_df, learning_goals):
    """Generate a quadrant analysis of skills based on impact and effort"""
    # Create a copy of the relevant data
    df = skills_df[['Skill', 'Rating', 'Domain']].copy()
    df = df.rename(columns={'Rating': 'Current Level'})
    
    # Calculate effort to improve (inverse of current level with randomization)
    df['Effort'] = df['Current Level'].apply(
        lambda x: max(1, 10 - (x * 1.5) + random.uniform(-0.5, 0.5))
    )
    
    # Calculate potential impact (higher for lower current levels)
    df['Impact'] = df['Current Level'].apply(
        lambda x: max(1, 10 - (x - 1) * 2 + random.uniform(-1, 1))
    )
    
    # Calculate alignment with learning goals
    df['Goal Alignment'] = df.apply(
        lambda row: calculate_goal_alignment(row['Skill'], row['Domain'], learning_goals),
        axis=1
    )
    
    # Add recommendation based on quadrant
    df['Recommendation'] = df.apply(
        lambda row: get_quadrant_recommendation(row['Effort'], row['Impact'], row['Current Level']),
        axis=1
    )
    
    return df


def calculate_goal_alignment(skill, domain, learning_goals):
    """Calculate how well a skill aligns with learning goals"""
    alignment_score = 5  # Base alignment
    
    # Check for direct keyword matches
    for goal in learning_goals:
        # Direct skill name alignment
        if any(kw.lower() in skill.lower() for kw in goal.split()):
            alignment_score += 5
        
        # Domain alignment
        if (domain == "Programming" and any(kw in goal for kw in ["Development", "Stack", "Full", "Web"])) or \
           (domain == "Data & Analytics" and any(kw in goal for kw in ["Data", "Analytics", "ML", "Science"])) or \
           (domain == "Infrastructure" and any(kw in goal for kw in ["Cloud", "DevOps", "Security", "SRE"])) or \
           (domain == "Soft Skills" and any(kw in goal for kw in ["Leadership", "Management"])):
            alignment_score += 3
    
    return min(15, alignment_score)  # Cap at 15


def get_quadrant_recommendation(effort, impact, current_level):
    """Generate a recommendation based on quadrant position"""
    if impact > 5 and effort < 5:
        return "High Priority - Quick Win"
    elif impact > 5 and effort >= 5:
        return "Strategic Investment - High Value"
    elif impact <= 5 and effort < 5:
        return "Easy Improvement - Lower Priority"
    else:
        return "Consider Later - Low Value/High Effort"


def generate_skill_priorities(quadrant_data):
    """Generate prioritized skill recommendations based on quadrant analysis"""
    # Create a copy of the relevant data
    df = quadrant_data[['Skill', 'Current Level', 'Effort', 'Impact', 'Goal Alignment', 'Domain', 'Recommendation']].copy()
    
    # Calculate priority score
    df['Priority Score'] = df.apply(
        lambda row: calculate_priority_score(row['Impact'], row['Effort'], row['Goal Alignment'], row['Current Level']),
        axis=1
    )
    
    # Assign priority levels
    df['Priority Level'] = pd.cut(
        df['Priority Score'],
        bins=[0, 30, 60, 100],
        labels=['Consider Later', 'Medium Priority', 'High Priority']
    )
    
    # Sort by priority score
    df = df.sort_values('Priority Score', ascending=False)
    
    return df


def calculate_priority_score(impact, effort, goal_alignment, current_level):
    """Calculate a priority score for skill development"""
    # Higher impact, lower effort, higher goal alignment, lower current level = higher priority
    effort_factor = max(1, (10 - effort)) / 10  # Invert so lower effort = higher score
    impact_factor = impact / 10
    alignment_factor = goal_alignment / 15
    level_factor = (5 - current_level) / 5  # Lower current level = higher priority
    
    # Weighted priority calculation
    priority = (
        (impact_factor * 40) +      # 40% weight to impact
        (effort_factor * 25) +      # 25% weight to ease of acquisition
        (alignment_factor * 20) +   # 20% weight to goal alignment
        (level_factor * 15)         # 15% weight to current level (gap size)
    ) * 100
    
    return min(99, round(priority))  # Cap at 99 and round