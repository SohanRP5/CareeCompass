import streamlit as st
import plotly.graph_objects as go
from career_advisor import get_career_recommendations
from utils import load_css, create_skill_rating_chart
import time

def main():
    load_css()
    
    st.title("🎯 AI Career Guidance System")
    
    with st.container():
        st.markdown("""
        <div class="header-container">
            <h2>Discover Your Ideal Career Path</h2>
            <p>Rate your skills below and let AI help you find the perfect career match!</p>
        </div>
        """, unsafe_allow_html=True)

    # Skills assessment
    skills = {
        "Programming": 0,
        "Data Analysis": 0,
        "Communication": 0,
        "Leadership": 0,
        "Problem Solving": 0,
        "Creativity": 0,
        "Project Management": 0,
        "Technical Writing": 0
    }

    st.subheader("💪 Rate Your Skills")
    st.markdown("Rate each skill from 1 to 5, where 1 is beginner and 5 is expert.")
    
    cols = st.columns(2)
    for idx, (skill, _) in enumerate(skills.items()):
        with cols[idx % 2]:
            skills[skill] = st.slider(f"{skill}", 1, 5, 3, key=skill)

    # Additional Information
    st.subheader("📝 Additional Information")
    experience_years = st.number_input("Years of Work Experience", 0, 50, 0)
    education_level = st.selectbox(
        "Education Level",
        ["High School", "Bachelor's", "Master's", "PhD", "Other"]
    )
    
    interests = st.text_area("Describe your interests and passions")

    if st.button("Get Career Recommendations", type="primary"):
        with st.spinner("🤔 Analyzing your profile..."):
            try:
                recommendations = get_career_recommendations(
                    skills,
                    experience_years,
                    education_level,
                    interests
                )
                
                # Display Results
                st.success("✨ Analysis Complete!")
                
                # Skills Radar Chart
                st.subheader("Your Skills Profile")
                fig = create_skill_rating_chart(skills)
                st.plotly_chart(fig, use_container_width=True)
                
                # Career Recommendations
                st.subheader("🎯 Recommended Career Paths")
                for idx, career in enumerate(recommendations['careers'], 1):
                    with st.expander(f"#{idx} {career['title']} - Match Score: {career['match_score']}%"):
                        st.markdown(f"""
                        **Description:** {career['description']}
                        
                        **Key Requirements:**
                        {career['requirements']}
                        
                        **Growth Potential:** {career['growth_potential']}
                        
                        **Next Steps:** {career['next_steps']}
                        """)
                
                # Development Plan
                st.subheader("📚 Recommended Development Plan")
                st.markdown(recommendations['development_plan'])
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="AI Career Guidance",
        page_icon="🎯",
        layout="wide"
    )
    main()
