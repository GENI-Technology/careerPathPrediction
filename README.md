# Career Path Recommendation System

![GENI Technology](geni.png)

## Overview
The Career Path Recommendation System is a demo application that helps users explore potential career paths based on their current occupation and skill set. The app uses a dataset of skills and occupations to provide recommendations and highlight skill gaps for the transition to a new career.

## About the Dataset
The dataset used in this app consists of skills and occupation data sourced from reliable databases, including O*NET. Each occupation is associated with various skills, with importance and level values provided for each skill.

## References
1. O*NET Database: [O*NET Online](https://www.onetonline.org/)
2. U.S. Department of Labor: [U.S. Department of Labor](https://www.dol.gov/)

## Model Used
This app uses the Cosine Similarity model to calculate the similarity between different occupations based on their skill requirements. This allows us to recommend career paths that require similar skill sets.

## Disclaimer
This application is a demo and should be used for informational purposes only. The recommendations provided are based on the available data and are meant to serve as a guide. Users are advised to perform further research and consider additional factors when making career decisions.

## Team Acknowledgement
This project is the output of the GENI research team. Our team is dedicated to providing insights and tools to help individuals navigate their career paths.

## Installation
To run this application locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/career-path-recommendation.git
    cd career-path-recommendation
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage
1. Select your current occupation from the dropdown menu.
2. Click the "Get Career Path Recommendations" button to view recommended career paths and skill gaps.

## Files
- `app.py`: The main Streamlit app script.
- `Skills.xlsx`: Dataset containing skills data.
- `Occupation Data.xlsx`: Dataset containing occupation descriptions.
- `image.png`: GENI Technology logo.
- `requirements.txt`: List of required Python packages.

## Deployment
To deploy the application on Streamlit Cloud:
1. Create a free account on [Streamlit Cloud](https://streamlit.io/cloud).
2. Upload your script, `requirements.txt`, and data files to a new app on Streamlit Cloud following their deployment instructions.

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please contact us at [your_email@example.com].
