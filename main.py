import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils import load_css, create_skill_rating_chart, get_skill_recommendations

def main():
    load_css()

    st.title("🎯 Technical Skills Assessment")

    with st.container():
        st.markdown("""
        <div class="header-container">
            <h2>Analyze Your Technical Skills</h2>
            <p>Rate your skills and get personalized development insights!</p>
        </div>
        """, unsafe_allow_html=True)

    # Technical Skills assessment
    technical_skills = {
        "Programming": {
            "Frontend Development": 0,
            "Backend Development": 0,
            "Database Management": 0,
            "Version Control": 0
        },
        "Data & Analytics": {
            "Data Analysis": 0,
            "Data Visualization": 0,
            "Machine Learning": 0,
            "Statistical Analysis": 0
        },
        "Infrastructure": {
            "Cloud Services": 0,
            "DevOps": 0,
            "System Administration": 0,
            "Security": 0
        }
    }

    st.subheader("💪 Rate Your Technical Skills")
    st.markdown("Rate each skill from 1 to 5, where 1 is beginner and 5 is expert.")

    # Create tabs for skill categories
    tabs = st.tabs(list(technical_skills.keys()))

    # Store all skill ratings
    all_ratings = {}

    # Create sliders for each category in tabs
    for tab, (category, skills) in zip(tabs, technical_skills.items()):
        with tab:
            st.subheader(f"{category} Skills")
            for skill in skills:
                rating = st.slider(
                    f"{skill}",
                    1, 5, 3,
                    key=f"{category}_{skill}"
                )
                all_ratings[skill] = rating

    # Additional Information
    st.subheader("📝 Experience Information")
    experience_years = st.number_input("Years of Technical Experience", 0, 50, 0)
    current_role = st.selectbox(
        "Current Role",
        ["Student", "Junior Developer", "Mid-level Developer", "Senior Developer", "Tech Lead", "Other"]
    )

    learning_goals = st.multiselect(
        "Select Your Learning Goals",
        [
            "Full-Stack Development",
            "Cloud Architecture",
            "Data Science",
            "DevOps",
            "Security",
            "Mobile Development"
        ]
    )

    if st.button("Analyze Skills", type="primary"):
        with st.spinner("📊 Analyzing your skills profile..."):
            # Create radar charts for each category
            for category, skills in technical_skills.items():
                st.subheader(f"{category} Profile")
                category_ratings = {skill: all_ratings[skill] for skill in skills}
                fig = create_skill_rating_chart(category_ratings)
                st.plotly_chart(fig, use_container_width=True)

            # Calculate and display skill gaps
            st.subheader("🎯 Skill Gap Analysis")
            col1, col2 = st.columns(2)

            with col1:
                # Calculate average skill level per category
                category_averages = {}
                for category, skills in technical_skills.items():
                    avg = sum(all_ratings[skill] for skill in skills) / len(skills)
                    category_averages[category] = avg

                # Create bar chart for category averages
                fig = px.bar(
                    x=list(category_averages.keys()),
                    y=list(category_averages.values()),
                    title="Category Proficiency Levels",
                    labels={"x": "Category", "y": "Average Skill Level"}
                )
                st.plotly_chart(fig)

            with col2:
                # Identify skill gaps
                skill_gaps = []
                for skill, rating in all_ratings.items():
                    if rating < 3:
                        skill_gaps.append({"skill": skill, "current_level": rating})

                if skill_gaps:
                    st.markdown("### Areas for Improvement")
                    for gap in skill_gaps:
                        st.markdown(f"- {gap['skill']}: Current Level {gap['current_level']}/5")
                else:
                    st.markdown("### Great job!")
                    st.markdown("You have a solid foundation across all skills!")

            # Get and display recommendations
            recommendations = get_skill_recommendations(
                all_ratings,
                experience_years,
                current_role,
                learning_goals
            )

            st.subheader("📚 Development Recommendations")
            for category, rec_list in recommendations.items():
                with st.expander(f"{category} Development Path"):
                    for rec in rec_list:
                        st.markdown(f"""
                        **{rec['title']}**
                        - Level: {rec['level']}
                        - Description: {rec['description']}
                        - Resources: {rec['resources']}
                        """)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Technical Skills Assessment",
        page_icon="🎯",
        layout="wide"
    )
    main()