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
