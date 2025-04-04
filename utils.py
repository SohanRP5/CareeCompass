import streamlit as st
import plotly.graph_objects as go

def load_css():
    """Load custom CSS and external libraries"""
    st.markdown("""
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def create_skill_rating_chart(skills):
    """Create an enhanced radar chart for skills visualization"""
    categories = list(skills.keys())
    values = list(skills.values())

    fig = go.Figure()

    # Add the skill trace with improved styling
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Skills',
        line_color='#4a69bd',
        line_width=3,
        fillcolor='rgba(74, 105, 189, 0.3)'
    ))
    
    # Add a reference line for the maximum level
    fig.add_trace(go.Scatterpolar(
        r=[5] * (len(categories) + 1),
        theta=categories + [categories[0]],
        fill=None,
        mode='lines',
        line_color='rgba(128, 128, 128, 0.2)',
        line_dash='dash',
        name='Maximum Level'
    ))

    # Customize the layout for better readability
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                linewidth=1,
                gridwidth=1,
                gridcolor='rgba(0, 0, 0, 0.1)',
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1', '2', '3', '4', '5']
            ),
            angularaxis=dict(
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            bgcolor='rgba(240, 240, 240, 0.2)'
        ),
        showlegend=False,
        margin=dict(l=80, r=80, t=20, b=80),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Roboto, sans-serif",
            size=12,
            color="#2c3e50"
        )
    )

    return fig

def get_skill_recommendations(skills, experience_years, current_role, learning_goals):
    """Generate detailed personalized skill development recommendations"""
    recommendations = {
        "Essential Skills": [],
        "Advanced Topics": [],
        "Specialization Paths": []
    }

    # Define skill thresholds and recommendations based on experience and role
    junior_threshold = 2
    mid_threshold = 3
    senior_threshold = 4
    
    # Define resources mapping by skill category
    resource_map = {
        "Frontend Development": "MDN Web Docs, Frontend Masters, CSS-Tricks",
        "Backend Development": "Node.js docs, Django Project, Spring Framework docs",
        "Database Management": "PostgreSQL tutorials, MongoDB University, SQL exercises",
        "Version Control/Git": "GitHub Learning Lab, Git documentation, Atlassian Git tutorials",
        "Mobile Development": "Google Developer Training, Apple Developer docs, Flutter tutorials",
        "Testing & QA": "Test Automation University, Software Testing Help, Cypress docs",
        "Data Analysis": "Kaggle, DataCamp, Analytics Vidhya",
        "Data Visualization": "D3.js gallery, Tableau Public, Observable",
        "Machine Learning": "TensorFlow tutorials, PyTorch docs, fast.ai",
        "Statistical Analysis": "Khan Academy, StatQuest, R for Data Science",
        "Big Data Technologies": "Apache Spark docs, Hadoop tutorials, Databricks Academy",
        "Business Intelligence": "Power BI learning center, Tableau tutorials, ThoughtSpot U",
        "Cloud Services": "AWS Training, Google Cloud Training, Azure Learn",
        "DevOps": "Docker docs, Kubernetes learning path, Jenkins tutorials",
        "System Administration": "Linux Academy, Red Hat docs, Microsoft Learn",
        "Cybersecurity": "TryHackMe, HackTheBox, OWASP resources",
        "Networking": "Cisco Learning Network, Wireshark University, Networking Academy",
        "Containerization": "Docker tutorials, Kubernetes docs, Red Hat OpenShift docs",
        "Technical Communication": "Technical Writing courses, Grammarly, HackMD tutorials",
        "Project Management": "PMI resources, Agile Alliance, Scrum Guides",
        "Problem Solving": "LeetCode, HackerRank, Project Euler",
        "Team Collaboration": "Atlassian Team Playbook, GitLab Team Handbook, Slack guides",
        "Time Management": "Pomodoro technique resources, Time blocking guides, Todoist",
        "Adaptability": "LinkedIn Learning courses, Pluralsight, Coursera certificates"
    }

    # Define more detailed recommendations
    detailed_recommendations = {
        "beginner": {
            "Frontend Development": "Focus on HTML, CSS basics and JavaScript fundamentals",
            "Backend Development": "Learn basic server concepts, RESTful APIs, and database connectivity",
            "Database Management": "Master SQL fundamentals and database design principles",
            "Version Control/Git": "Practice Git basics: commit, push, pull, and branch management",
            "Cloud Services": "Understand fundamental cloud concepts and basic AWS/Azure services",
            "DevOps": "Learn CI/CD concepts and basic pipeline construction",
            "Data Analysis": "Build skills in data cleaning, exploration, and basic statistics",
            "Machine Learning": "Learn foundations of ML algorithms and basic model training"
        },
        "intermediate": {
            "Frontend Development": "Master modern JavaScript frameworks like React, Vue or Angular",
            "Backend Development": "Implement authentication, API security, and advanced server patterns",
            "Database Management": "Optimize queries, design schemas, and implement migrations",
            "Version Control/Git": "Practice advanced Git flows, rebasing, and team collaboration",
            "Cloud Services": "Implement serverless architectures and multi-region deployments",
            "DevOps": "Design robust CI/CD pipelines and infrastructure as code",
            "Data Analysis": "Apply advanced statistical methods and build data processing pipelines",
            "Machine Learning": "Implement and fine-tune complex ML models for specific domains"
        },
        "advanced": {
            "Frontend Development": "Architect large-scale applications, optimize performance, and implement micro-frontends",
            "Backend Development": "Design scalable services, implement caching strategies, and manage high-traffic systems",
            "Database Management": "Implement sharding, replication, and high-availability solutions",
            "Version Control/Git": "Customize Git workflows for enterprise teams and implement advanced branching strategies",
            "Cloud Services": "Design multi-cloud architectures and implement cloud-native solutions",
            "DevOps": "Implement observability systems and manage complex Kubernetes deployments",
            "Data Analysis": "Build real-time analytics systems and advanced data models",
            "Machine Learning": "Develop custom AI solutions and deploy models at scale"
        }
    }

    # Essential Skills Recommendations (for skills with low ratings)
    for skill, rating in skills.items():
        if rating <= junior_threshold:
            skill_description = detailed_recommendations.get("beginner", {}).get(
                skill, f"Build a strong foundation in {skill}")
            skill_resources = resource_map.get(skill, "Online courses, tutorials, and hands-on projects")
            
            recommendations["Essential Skills"].append({
                "title": f"Strengthen {skill}",
                "level": "Fundamental",
                "description": skill_description,
                "resources": skill_resources
            })

    # Advanced Topics (based on experience and learning goals)
    if experience_years >= 2:
        for goal in learning_goals:
            # Map learning goals to related skills
            related_skills = []
            
            if "Full-Stack" in goal:
                related_skills = ["Frontend Development", "Backend Development", "Database Management"]
            elif "Cloud" in goal:
                related_skills = ["Cloud Services", "DevOps", "System Administration"]
            elif "Data Science" in goal:
                related_skills = ["Data Analysis", "Machine Learning", "Statistical Analysis"]
            elif "DevOps" in goal:
                related_skills = ["DevOps", "Containerization", "Cloud Services"]
            elif "Security" in goal:
                related_skills = ["Cybersecurity", "System Administration", "Networking"]
            elif "Mobile" in goal:
                related_skills = ["Mobile Development", "Frontend Development", "Testing & QA"]
            else:
                related_skills = [goal]  # Default to the goal itself
            
            for skill in related_skills:
                if skill in skills and skills.get(skill, 0) >= mid_threshold:
                    skill_description = detailed_recommendations.get("intermediate", {}).get(
                        skill, f"Deep dive into {skill} concepts and best practices")
                    skill_resources = resource_map.get(skill, "Advanced workshops and certification programs")
                    
                    recommendations["Advanced Topics"].append({
                        "title": f"Master {skill}",
                        "level": "Advanced",
                        "description": skill_description,
                        "resources": skill_resources
                    })

    # Specialization Paths (for senior roles)
    if current_role in ["Mid-level Developer", "Senior Developer", "Tech Lead", "Manager"]:
        for goal in learning_goals:
            # Create specialization recommendations based on career goals
            if goal == "Technical Leadership":
                recommendations["Specialization Paths"].append({
                    "title": "Engineering Leadership Path",
                    "level": "Expert",
                    "description": "Develop technical leadership skills to guide teams and make architectural decisions",
                    "resources": "Leadership workshops, architectural decision-making courses, and mentorship programs"
                })
            elif "Architecture" in goal:
                recommendations["Specialization Paths"].append({
                    "title": "Solution Architecture Mastery",
                    "level": "Expert",
                    "description": "Learn to design and implement large-scale technical solutions across multiple domains",
                    "resources": "AWS/Azure/GCP architecture certifications, system design courses, and case studies"
                })
            else:
                # General specialization based on the goal
                recommendations["Specialization Paths"].append({
                    "title": f"{goal} Specialization",
                    "level": "Expert",
                    "description": f"Become an expert in {goal} to lead initiatives and drive innovation",
                    "resources": f"Industry certifications, conference speaking opportunities, and {goal.lower()} communities"
                })

    # Ensure we have at least some recommendations in each category
    if not recommendations["Essential Skills"]:
        recommendations["Essential Skills"].append({
            "title": "Core Technical Foundations",
            "level": "Fundamental",
            "description": "Even experienced professionals benefit from refreshing fundamentals",
            "resources": "Interactive tutorials, coding challenges, and foundation courses"
        })
    
    if not recommendations["Advanced Topics"] and experience_years >= 1:
        recommendations["Advanced Topics"].append({
            "title": "Technical Growth Areas",
            "level": "Advanced",
            "description": "Identify areas for growth based on industry trends and your interests",
            "resources": "Technology blogs, conference talks, and specialized online courses"
        })
    
    return recommendations