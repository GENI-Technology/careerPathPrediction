import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

# Load the logo image
logo_image = 'geni.png'

@st.cache
def load_data():
    skills_df = pd.read_excel('Skills.xlsx', engine='openpyxl')
    occupation_df = pd.read_excel('Occupation Data.xlsx', engine='openpyxl')
    return skills_df, occupation_df

@st.cache
def process_data(skills_df, occupation_df):
    # Merge the data
    merged_df = pd.merge(skills_df, occupation_df, on='O*NET-SOC Code', how='inner')
    
    # Pivot the data to get skill importance and level for each occupation
    pivot_df = merged_df.pivot_table(
        index=['O*NET-SOC Code', 'Title_y', 'Description'], 
        columns='Element Name', 
        values='Data Value', 
        aggfunc='mean'
    ).reset_index()
    
    # Extract skill-related columns
    skill_columns = pivot_df.columns[3:]
    
    # Calculate the cosine similarity between occupations
    skill_matrix = pivot_df[skill_columns].fillna(0)
    cosine_sim = cosine_similarity(skill_matrix)
    
    # Convert the similarity matrix to a DataFrame
    similarity_df = pd.DataFrame(cosine_sim, index=pivot_df['Title_y'], columns=pivot_df['Title_y'])
    
    return pivot_df, similarity_df

def recommend_career_paths(occupation, similarity_df, top_n=5):
    if occupation in similarity_df.index:
        similar_occupations = similarity_df[occupation].sort_values(ascending=False).head(top_n + 1)
        similar_occupations = similar_occupations.drop(occupation)
        return similar_occupations
    else:
        return None

def plot_skill_gaps(skill_gaps_sorted):
    fig, ax = plt.subplots(figsize=(10, 6))
    skill_gaps_sorted.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_xlabel('Skill Gap')
    ax.set_title('Skill Gaps to Transition to the Recommended Occupation')
    st.pyplot(fig)

def plot_skill_improvement(skill, gap):
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.barh(skill, gap, color='skyblue')
    ax.set_xlim(0, 1)
    ax.set_title(f'Improvement Needed: {skill}')
    st.pyplot(fig)

# Load and process data
skills_df, occupation_df = load_data()
pivot_df, similarity_df = process_data(skills_df, occupation_df)

# Streamlit app
st.image(logo_image, width=200)
st.title("Career Path Recommendation System")

st.markdown("""
### About the Dataset
The dataset used in this app consists of skills and occupation data sourced from reliable databases, including O*NET. Each occupation is associated with various skills, with importance and level values provided for each skill. 

### References
1. O*NET Database: [O*NET Online](https://www.onetonline.org/)
2. U.S. Department of Labor: [U.S. Department of Labor](https://www.dol.gov/)

### Model Used
This app uses the Cosine Similarity model to calculate the similarity between different occupations based on their skill requirements. This allows us to recommend career paths that require similar skill sets.

### Disclaimer
This application is a demo and should be used for informational purposes only. The recommendations provided are based on the available data and are meant to serve as a guide. Users are advised to perform further research and consider additional factors when making career decisions. The current model accuracy is not optimal and may not always provide the most accurate career path recommendations.
""")

# User input for current occupation
occupation = st.selectbox("Select your current occupation:", similarity_df.index)

if st.button("Get Career Path Recommendations"):
    # Get recommended career paths
    recommended_paths = recommend_career_paths(occupation, similarity_df, top_n=5)
    
    if recommended_paths is not None:
        st.subheader(f"Recommended career paths for {occupation}:")
        for idx, (rec_occ, score) in enumerate(recommended_paths.items(), start=1):
            st.write(f"{idx}. {rec_occ} (Similarity Score: {score:.3f})")

        # Highlight skill gaps for the top recommended career path
        top_recommended_occupation = recommended_paths.index[0]
        current_occupation_skills = pivot_df[pivot_df['Title_y'] == occupation].iloc[:, 3:].reset_index(drop=True)
        recommended_occupation_skills = pivot_df[pivot_df['Title_y'] == top_recommended_occupation].iloc[:, 3:].reset_index(drop=True)
        skill_gaps = recommended_occupation_skills - current_occupation_skills
        skill_gaps = skill_gaps.T  # Transpose for better readability
        skill_gaps.columns = ['Skill Gap']
        skill_gaps_sorted = skill_gaps.sort_values(by='Skill Gap', ascending=False)

        st.subheader(f"\nSkill gaps to transition from {occupation} to {top_recommended_occupation}:")
        st.write(skill_gaps_sorted)

        st.subheader("Visual representation of the skill gaps:")
        plot_skill_gaps(skill_gaps_sorted)

        st.markdown("""
        ### Skill Improvement Plan
        Based on the identified skill gaps, here is a plan to help you improve the necessary skills for your desired career transition:
        """)

        for skill, gap in skill_gaps_sorted.iterrows():
            st.markdown(f"**{skill}**: {gap.values[0]:.4f}")
            st.markdown(f"**Description**: To excel in {skill}, you need to improve your understanding and application of this skill.")
            st.markdown(f"**Steps to Improve**:")
            st.markdown(f"1. **Self-Assessment**: Evaluate your current proficiency level in {skill}. Identify specific areas where you need improvement.")
            st.markdown(f"2. **Learning Resources**: Utilize online courses, tutorials, and books to learn and enhance your {skill} skills.")
            st.markdown(f"3. **Practical Application**: Apply what you learn through practice, projects, or real-world scenarios.")
            st.markdown(f"4. **Feedback**: Seek feedback from mentors, peers, or professionals to understand your progress and areas for further improvement.")
            st.markdown(f"**Recommended Resources**:")
            st.markdown(f"- **Online Courses**: Coursera, Udemy, LinkedIn Learning, edX")
            st.markdown(f"- **Books**: Look for highly-rated books on {skill} on Amazon or your local library")
            st.markdown(f"- **Workshops**: Attend workshops or webinars related to {skill}")
            st.markdown(f"- **Mentorship**: Find a mentor who excels in {skill} and can provide guidance")
            plot_skill_improvement(skill, gap.values[0])
            st.markdown(f"---")

    else:
        st.write("Occupation not found in the dataset.")
