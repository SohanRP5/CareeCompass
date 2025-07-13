import streamlit as st
import plotly.graph_objects as go

def load_css():
    with open('styles.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def create_skill_rating_chart(skills_data):
    categories = list(skills_data.keys())
    values = list(skills_data.values())
    
    fig = go.Figure(data=[

    go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    )
    ])
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False
    )
    return fig

def get_skill_recommendations(ratings, experience, role, goals):
    recommendations = {
        "Technical Skills": [
            {
                "title": "Strengthen Programming Skills",
                "level": "Intermediate",
                "description": "Focus on building stronger programming fundamentals",
                "resources": "Online courses, coding challenges"
            }
        ],
        "Career Development": [
            {
                "title": "Professional Growth",
                "level": "All Levels",
                "description": "Enhance your professional network",
                "resources": "LinkedIn, tech conferences, meetups"
            }
        ]
    }
    return recommendations