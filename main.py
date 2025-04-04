import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import random
import pandas as pd
import time
from utils import load_css, create_skill_rating_chart, get_skill_recommendations
from analytics_report import generate_analytics_report
from data_analytics_guide import add_analytics_document_tab

def main():
    load_css()
    
    # App header with animation effect
    with st.container():
        st.markdown("""
        <div class="header-container">
            <h2>💻 Tech Career Compass</h2>
            <p>Your interactive guide to technical skills assessment and career growth</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation tabs for the entire application
    app_tabs = st.tabs(["🔍 Skills Assessment", "📊 Analytics Dashboard", "🚀 Career Roadmap", "📚 Documentation"])
    
    with app_tabs[0]:  # Skills Assessment Tab
        st.markdown("""
        <div class="card-container">
            <h3>Rate Your Technical Proficiency</h3>
            <p>Assess your skills from 1 (beginner) to 5 (expert) in various technical domains</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Technical Skills assessment with enhanced categories
        technical_skills = {
            "Programming": {
                "Frontend Development": 0,
                "Backend Development": 0,
                "Database Management": 0,
                "Version Control/Git": 0,
                "Mobile Development": 0,
                "Testing & QA": 0
            },
            "Data & Analytics": {
                "Data Analysis": 0,
                "Data Visualization": 0,
                "Machine Learning": 0,
                "Statistical Analysis": 0,
                "Big Data Technologies": 0,
                "Business Intelligence": 0
            },
            "Infrastructure": {
                "Cloud Services": 0,
                "DevOps": 0,
                "System Administration": 0,
                "Cybersecurity": 0,
                "Networking": 0,
                "Containerization": 0
            },
            "Soft Skills": {
                "Technical Communication": 0,
                "Project Management": 0,
                "Problem Solving": 0,
                "Team Collaboration": 0,
                "Time Management": 0,
                "Adaptability": 0
            }
        }
        
        # Create tabs for skill categories
        skill_tabs = st.tabs(list(technical_skills.keys()))
        
        # Store all skill ratings
        all_ratings = {}
        
        # Create enhanced sliders for each category in tabs
        for tab, (category, skills) in zip(skill_tabs, technical_skills.items()):
            with tab:
                st.markdown(f"<h3>{category} Skills Assessment</h3>", unsafe_allow_html=True)
                
                # Visual skill level guide
                st.markdown("""
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                    <div><span class="skill-level-dot beginner"></span> 1: Beginner</div>
                    <div><span class="skill-level-dot intermediate"></span> 2-3: Intermediate</div>
                    <div><span class="skill-level-dot advanced"></span> 4: Advanced</div>
                    <div><span class="skill-level-dot expert"></span> 5: Expert</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Two columns layout for skills
                col1, col2 = st.columns(2)
                skill_list = list(skills.keys())
                half = len(skill_list) // 2
                
                # First column of skills
                with col1:
                    for skill in skill_list[:half]:
                        rating = st.slider(
                            f"{skill}",
                            1, 5, 3,
                            key=f"{category}_{skill}"
                        )
                        all_ratings[skill] = rating
                
                # Second column of skills
                with col2:
                    for skill in skill_list[half:]:
                        rating = st.slider(
                            f"{skill}",
                            1, 5, 3,
                            key=f"{category}_{skill}"
                        )
                        all_ratings[skill] = rating
        
        # Additional Information with enhanced UI
        st.markdown("""
        <div class="card-container">
            <h3>📝 Professional Background</h3>
            <p>Help us understand your experience and career aspirations</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            experience_years = st.number_input("Years of Technical Experience", 0, 50, 3)
            education_level = st.selectbox(
                "Highest Education Level",
                ["High School", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "PhD", "Self-taught"]
            )
        
        with col2:
            current_role = st.selectbox(
                "Current Role",
                ["Student", "Junior Developer", "Mid-level Developer", "Senior Developer", "Tech Lead", "Manager", "Other"]
            )
            industry = st.selectbox(
                "Industry Sector",
                ["Technology", "Finance", "Healthcare", "Education", "E-commerce", "Manufacturing", "Other"]
            )
        
        # Interest areas with enhanced UI
        st.markdown("<h3>🎯 Focus Areas</h3>", unsafe_allow_html=True)
        learning_goals = st.multiselect(
            "Select Your Career & Learning Goals",
            [
                "Full-Stack Development",
                "Cloud Architecture",
                "Data Science & ML",
                "DevOps & SRE",
                "Cybersecurity",
                "Mobile Development",
                "UI/UX Design",
                "Technical Leadership",
                "Blockchain Development",
                "AR/VR Development",
                "Game Development",
                "IoT Development"
            ]
        )
        
        # Analysis button with enhanced UI
        if st.button("Generate Comprehensive Analysis", type="primary"):
            # Progress bar for visual feedback
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            with st.spinner("📊 Generating your personalized skills profile..."):
                st.markdown("""
                <div class="card-container">
                    <h2>Your Technical Skills Analysis</h2>
                    <p>Comprehensive breakdown of your current technical proficiency</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Create enhanced radar charts for each category
                for category, skills in technical_skills.items():
                    st.markdown(f"""
                    <div class="focus-area">
                        <h3>{category} Profile</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    category_ratings = {skill: all_ratings[skill] for skill in skills}
                    fig = create_skill_rating_chart(category_ratings)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Enhanced Skill Gap Analysis
                st.markdown("""
                <div class="card-container">
                    <h2>🎯 Skill Gap Analysis</h2>
                    <p>Areas of strength and opportunities for growth</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Enhanced category averages visualization
                    category_averages = {}
                    for category, skills in technical_skills.items():
                        avg = sum(all_ratings[skill] for skill in skills) / len(skills)
                        category_averages[category] = avg
                    
                    # Create enhanced bar chart for category averages
                    fig = px.bar(
                        x=list(category_averages.keys()),
                        y=list(category_averages.values()),
                        title="Domain Proficiency Overview",
                        labels={"x": "Domain", "y": "Average Skill Level"},
                        color=list(category_averages.values()),
                        color_continuous_scale=px.colors.sequential.Viridis,
                        template="plotly_white"
                    )
                    fig.update_layout(
                        coloraxis_showscale=False,
                        height=400,
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Enhanced skill gaps identification with visual indicators
                    strengths = []
                    skill_gaps = []
                    
                    for skill, rating in all_ratings.items():
                        if rating >= 4:
                            strengths.append({"skill": skill, "level": rating})
                        elif rating <= 2:
                            skill_gaps.append({"skill": skill, "level": rating})
                    
                    # Display strengths
                    st.markdown("<h3>💪 Your Strengths</h3>", unsafe_allow_html=True)
                    if strengths:
                        for strength in strengths[:5]:  # Show top 5 strengths
                            level_percentage = (strength["level"] / 5) * 100
                            st.markdown(f"""
                            <p>{strength["skill"]}</p>
                            <div class="skill-bar">
                                <div class="skill-fill" style="width: {level_percentage}%;"></div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Continue developing your skills to identify clear strengths!")
                    
                    # Display improvement areas
                    st.markdown("<h3>🚀 Growth Opportunities</h3>", unsafe_allow_html=True)
                    if skill_gaps:
                        for gap in skill_gaps[:5]:  # Show top 5 gaps
                            level_percentage = (gap["level"] / 5) * 100
                            st.markdown(f"""
                            <p>{gap["skill"]}</p>
                            <div class="skill-bar">
                                <div class="skill-fill" style="width: {level_percentage}%;"></div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("Great job! You have a solid foundation across all skills!")
                
                # Get and display enhanced recommendations
                recommendations = get_skill_recommendations(
                    all_ratings,
                    experience_years,
                    current_role,
                    learning_goals
                )
                
                st.markdown("""
                <div class="card-container">
                    <h2>📚 Personalized Development Plan</h2>
                    <p>Tailored recommendations based on your skills and goals</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced recommendation display with accordion
                for category, rec_list in recommendations.items():
                    with st.expander(f"{category} Development Path", expanded=True):
                        for rec in rec_list:
                            st.markdown(f"""
                            <div class="focus-area">
                                <h4>{rec['title']}</h4>
                                <p><strong>Level:</strong> {rec['level']}</p>
                                <p><strong>Description:</strong> {rec['description']}</p>
                                <p><strong>Resources:</strong> {rec['resources']}</p>
                            </div>
                            """, unsafe_allow_html=True)
    
    with app_tabs[1]:  # Analytics Dashboard Tab
        st.markdown("""
        <div class="card-container">
            <h2>📈 Skills Analytics Dashboard</h2>
            <p>Visual insights to track your technical growth with detailed data analytics</p>
        </div>
        """, unsafe_allow_html=True)

        # Add tabs for different analytics views
        analytics_tabs = st.tabs(["📊 Quick Overview", "📈 Comprehensive Report"])
        
        with analytics_tabs[0]:  # Quick Overview Tab
            # Basic skill statistics for quick view
            if len(all_ratings) > 0:  # Only show if skills have been rated
                # Industry comparison (simulated data)
                st.subheader("Industry Benchmarks Comparison")
                st.markdown("""
                <div class="chart-explanation">
                    <p><strong>Chart Type:</strong> Grouped Bar Chart</p>
                    <p><strong>Purpose:</strong> Compares your skill ratings against industry average benchmarks.</p>
                    <p><strong>How to interpret:</strong> Bars higher than the industry average indicate areas where you excel.
                    Bars below industry average suggest potential growth opportunities.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate random industry data for visualization
                industry_data = {skill: min(5, max(1, rating + random.uniform(-1, 1))) 
                                for skill, rating in list(all_ratings.items())[:8]}  # Use a subset
                
                # Create a comparison dataframe
                comparison_data = {
                    'Skill': list(industry_data.keys()),
                    'Your Rating': [all_ratings.get(skill, 0) for skill in industry_data.keys()],
                    'Industry Average': list(industry_data.values())
                }
                df = pd.DataFrame(comparison_data)
                
                # Create a grouped bar chart
                fig = px.bar(
                    df, 
                    x='Skill', 
                    y=['Your Rating', 'Industry Average'],
                    barmode='group',
                    color_discrete_sequence=['#4a69bd', '#6c757d'],
                    template="plotly_white",
                    title="Your Skills vs. Industry Benchmarks"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Skill distribution with explanation
                st.subheader("Skill Level Distribution")
                st.markdown("""
                <div class="chart-explanation">
                    <p><strong>Chart Type:</strong> Donut Chart</p>
                    <p><strong>Purpose:</strong> Shows the distribution of your skills across different proficiency levels.</p>
                    <p><strong>How to interpret:</strong> Larger segments indicate more skills at that level.
                    A balanced distribution or skew toward higher levels indicates a well-rounded skill profile.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Count ratings by level
                if all_ratings:
                    rating_counts = {'Beginner (1)': 0, 'Basic (2)': 0, 'Intermediate (3)': 0, 'Advanced (4)': 0, 'Expert (5)': 0}
                    for rating in all_ratings.values():
                        if rating == 1:
                            rating_counts['Beginner (1)'] += 1
                        elif rating == 2:
                            rating_counts['Basic (2)'] += 1
                        elif rating == 3:
                            rating_counts['Intermediate (3)'] += 1
                        elif rating == 4:
                            rating_counts['Advanced (4)'] += 1
                        elif rating == 5:
                            rating_counts['Expert (5)'] += 1
                    
                    # Create a pie chart
                    fig = px.pie(
                        values=list(rating_counts.values()),
                        names=list(rating_counts.keys()),
                        title="Distribution of Your Skill Levels",
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        hole=0.4
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Rate your skills in the Assessment tab to see your skill distribution")
            else:
                st.info("Please complete the Skills Assessment to view analytics")
                
        with analytics_tabs[1]:  # Comprehensive Report Tab
            if len(all_ratings) > 0:
                # Pass all the necessary data to generate a comprehensive analytics report
                generate_analytics_report(
                    all_ratings,
                    experience_years,
                    education_level,
                    current_role,
                    learning_goals
                )
            else:
                st.info("Please complete the Skills Assessment to view the comprehensive analytics report")
    
    with app_tabs[2]:  # Career Roadmap Tab
        st.markdown("""
        <div class="card-container">
            <h2>🚀 Career Growth Roadmap</h2>
            <p>Visualize your career journey and future growth options</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show career path visualization based on current role
        role_paths = {
            "Student": ["Junior Developer", "Mid-level Developer", "Senior Developer", "Tech Lead", "CTO"],
            "Junior Developer": ["Mid-level Developer", "Senior Developer", "Tech Lead", "Engineering Manager", "CTO"],
            "Mid-level Developer": ["Senior Developer", "Tech Lead", "Engineering Manager", "Director of Engineering", "CTO"],
            "Senior Developer": ["Tech Lead", "Engineering Manager", "Product Architect", "Director of Engineering", "CTO"],
            "Tech Lead": ["Engineering Manager", "Product Architect", "Director of Engineering", "VP of Engineering", "CTO"],
            "Manager": ["Director of Engineering", "VP of Engineering", "CTO", "Chief Digital Officer", "CEO"],
            "Other": ["Specialist", "Consultant", "Team Lead", "Department Head", "Executive"]
        }
        
        if current_role in role_paths:
            st.subheader(f"Career Progression Path from {current_role}")
            st.markdown("""
            <div class="chart-explanation">
                <p><strong>Chart Type:</strong> Timeline Chart</p>
                <p><strong>Purpose:</strong> Visualizes your potential career progression path based on your current role.</p>
                <p><strong>How to interpret:</strong> Each point represents a career milestone, with approximate years of experience
                required to reach each level. The path is customized based on your current position.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a career path visualization
            career_data = {
                'Position': [current_role] + role_paths[current_role],
                'Level': list(range(1, len(role_paths[current_role]) + 2)),
                'Years': [0, 2, 5, 8, 12, 15][:len(role_paths[current_role]) + 1]
            }
            df = pd.DataFrame(career_data)
            
            fig = px.line(
                df, 
                x='Years', 
                y='Level', 
                text='Position',
                markers=True,
                line_shape='spline',
                template="plotly_white"
            )
            
            fig.update_traces(textposition="top center")
            fig.update_layout(
                title="Your Technical Career Timeline",
                xaxis_title="Experience (Years)",
                yaxis_title="Career Level",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Certification recommendations based on learning goals
            if learning_goals:
                st.subheader("Recommended Certifications")
                st.markdown("""
                <div class="chart-explanation">
                    <p><strong>Purpose:</strong> Provides targeted certification recommendations based on your selected learning goals.</p>
                    <p><strong>How to use:</strong> These certifications are industry-recognized credentials that can help validate your
                    skills and accelerate your career progression in your chosen focus areas.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Sample certifications map
                cert_map = {
                    "Full-Stack Development": ["AWS Certified Developer", "Full Stack Web Developer", "JavaScript Full Stack Certification"],
                    "Cloud Architecture": ["AWS Solutions Architect", "Google Cloud Architect", "Azure Solutions Architect"],
                    "Data Science & ML": ["TensorFlow Developer Certificate", "Microsoft Certified: Azure Data Scientist", "IBM Data Science Professional"],
                    "DevOps & SRE": ["AWS DevOps Engineer", "Certified Kubernetes Administrator", "Docker Certified Associate"],
                    "Cybersecurity": ["CompTIA Security+", "Certified Ethical Hacker", "CISSP"],
                    "Mobile Development": ["Google Associate Android Developer", "Apple Certified iOS Developer", "React Native Certification"],
                    "UI/UX Design": ["Certified User Experience Professional", "Adobe XD Certification", "Google UX Design Certificate"],
                    "Technical Leadership": ["Scrum Master Certification", "Project Management Professional (PMP)", "Certified Agile Leadership"],
                    "Blockchain Development": ["Certified Blockchain Developer", "Ethereum Developer Certification", "Hyperledger Fabric Developer"],
                    "AR/VR Development": ["Unity Certified Developer", "Unreal Engine Certification", "AR/VR Design & Development Certificate"],
                    "Game Development": ["Unity Certified Programmer", "Unreal Engine Developer", "Game Development & Design Certificate"],
                    "IoT Development": ["IoT Developer Certificate", "Microsoft Certified: Azure IoT Developer", "AWS IoT Specialization"]
                }
                
                for goal in learning_goals:
                    if goal in cert_map:
                        st.markdown(f"""
                        <div class="focus-area">
                            <h4>{goal}</h4>
                            <ul>
                                {"".join([f"<li>{cert}</li>" for cert in cert_map[goal]])}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Select learning goals in the Assessment tab to see certification recommendations")

    with app_tabs[3]:  # Documentation Tab
        add_analytics_document_tab()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Tech Career Compass",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()