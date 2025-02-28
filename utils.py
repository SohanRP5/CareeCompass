import streamlit as st
import plotly.graph_objects as go

def load_css():
    st.markdown("""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    """, unsafe_allow_html=True)

    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def create_skill_rating_chart(skills):
    """Create a radar chart for skills visualization"""
    categories = list(skills.keys())
    values = list(skills.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Skills',
        line_color='#FF4B4B',
        fillcolor='rgba(255, 75, 75, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return fig

def get_skill_recommendations(skills, experience_years, current_role, learning_goals):
    """Generate personalized skill development recommendations"""
    recommendations = {
        "Essential Skills": [],
        "Advanced Topics": [],
        "Specialization Paths": []
    }

    # Define skill thresholds and recommendations based on experience and role
    junior_threshold = 2
    mid_threshold = 3
    senior_threshold = 4

    # Essential Skills Recommendations
    for skill, rating in skills.items():
        if rating <= junior_threshold:
            recommendations["Essential Skills"].append({
                "title": f"Strengthen {skill}",
                "level": "Fundamental",
                "description": f"Build a strong foundation in {skill}",
                "resources": "Online courses, tutorials, and hands-on projects"
            })

    # Advanced Topics
    if experience_years >= 2:
        for goal in learning_goals:
            recommendations["Advanced Topics"].append({
                "title": f"Master {goal}",
                "level": "Advanced",
                "description": f"Deep dive into {goal} concepts and best practices",
                "resources": "Advanced workshops, certification programs, and real-world projects"
            })

    # Specialization Paths
    if current_role in ["Mid-level Developer", "Senior Developer", "Tech Lead"]:
        for goal in learning_goals:
            recommendations["Specialization Paths"].append({
                "title": f"{goal} Specialization",
                "level": "Expert",
                "description": f"Become an expert in {goal}",
                "resources": "Industry certifications, advanced projects, and mentorship opportunities"
            })

    return recommendations