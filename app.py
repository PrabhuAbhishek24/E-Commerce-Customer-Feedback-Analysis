import streamlit as st
from textblob import TextBlob
import re
import altair as alt
import pandas as pd
import joblib


# Function to handle negations
def negation_handler(text):
    negations = [
        "not", "no", "never", "none", "nothing", "neither", "nobody", "disappointing",
        "lack", "without", "neither", "hardly", "barely", "seldom", "few", "nevermore",
        "nowhere", "no one", "nothingness", "neglect", "absent", "refuse", "against",
        "dislike", "unpleasant", "unhappy", "unsatisfactory", "dissatisfied", "unfavorable",
        "inadequate", "imperfect", "problematic", "not at all", "not really", "not quite",
        "not much", "no longer", "not any", "not a single", "unacceptable", "unwanted",
        "not good", "not enough", "not pleasant", "untrustworthy", "not true", "not right",
        "bastard", "bullshit"
    ]
    neg_pattern = re.compile(r'\b(?:' + '|'.join(negations) + r')\b', re.IGNORECASE)

    words = text.split()
    negated = False
    processed_words = []
    for word in words:
        if neg_pattern.match(word):
            negated = True
            processed_words.append(word)
        elif negated and word.isalpha():
            processed_words.append("neg_" + word)
            negated = False
        else:
            processed_words.append(word)

    return ' '.join(processed_words)


# Function to analyze sentiment
def analyze_sentiment(text):
    processed_text = negation_handler(text)
    sentences = TextBlob(processed_text).sentences
    sentiment_score = sum([sentence.sentiment.polarity for sentence in sentences]) / len(sentences)
    return sentiment_score


# Function to map polarity score to a 1-5 scale
def map_polarity_to_scale(polarity):
    if polarity == 0.00:
        return 3
    elif 0.0001 <= polarity <= 0.49:
        return 4
    elif 0.5 <= polarity <= 1:
        return 5
    elif -0.49 <= polarity <= -0.0001:
        return 2
    elif -1 <= polarity < 0:
        return 1


# Function to get emoji based on score
def get_emoji_for_score(score):
    if score == 1:
        return "😢 Very sad and crying"
    elif score == 2:
        return "😞 Sad and dull"
    elif score == 3:
        return "😐 Neutral"
    elif score == 4:
        return "😊 Happy"
    elif score == 5:
        return "😍 Very happy"


# Custom CSS for better styling and logo placement
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #f9f9f9;
        }
        .main-title {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            color: #000000;
        }
        .sub-title {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #fffff;
        }
        .feedback-box {
            border-radius: 10px;
            background-color: #ffffff;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background-color: #F17925;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 16px;
            margin-top: 20px;
        }
        .stTextArea textarea {
            font-size: 1.1em;
        }
        .logo-container {
            text-align: right;
        }
        .sidebar .sidebar-content {
            background-color: #f2f2f2;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


add_custom_css()

# Left sidebar for navigation
with st.sidebar:
    st.markdown("<h2>Navigation</h2>", unsafe_allow_html=True)
    selected = st.selectbox(
        "Select Section",
        [
            "📖 About Project",
            "🔍 Feedback Analysis",
            "📊 Dashboard Analysis",  # New option added
            "📈 BI Analysis"  # New section for BI Analysis
        ]
    )
    st.markdown("---")  # Adds a horizontal line
# "About Project" section
if selected == '📖 About Project':
    # CSS to position the logo at the top-right corner
    st.markdown(
        """
        <style>
        .logo {
            position: absolute;
            top: 0;
            right: 0;
            width: 150px;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Display the logo
    st.image("_1523354169_521_amazon-preview (1).jpg", use_column_width=False, width=150)
    st.title("E-Commerce Customer Feedback Analysis")
    st.info("About Project")
    st.success(
        """This project focuses on analyzing customer feedback from Amazon, aiming to uncover insights about customer satisfaction, sentiment trends, and areas for improvement. As customer reviews play a crucial role in shaping e-commerce success, this analysis is vital for businesses to understand customer sentiments and improve their offerings.""")
    st.info("Why it is needed?")
    st.success("""Understanding customer sentiment is essential for e-commerce platforms like Amazon. With thousands of reviews generated daily, manual analysis becomes impossible. Automated sentiment analysis helps extract meaningful insights from the vast amount of data, allowing businesses to:
               1. Identify products that need improvement.
               2. Understand market trends through customer feedback.
               3. Enhance customer experience.""")

    st.info("Project Overview:")
    st.success(
        """We have developed a Long Short-Term Memory (LSTM) model that accurately captures sentiment from customer reviews. The LSTM model is trained on Amazon reviews, making it capable of identifying emotions and opinions embedded in the text. Additionally, we use a sentiment analysis algorithm to categorize feedback as positive, neutral, or negative, providing a deeper understanding of customer sentiments.""")
    st.info("Interface Used:")
    st.success(
        """The project utilizes Streamlit to create an interactive and user-friendly web interface for real-time feedback analysis, making it easy to view sentiment predictions and other insights.""")

    # Developer credits - More visually appealing
    st.title("Developed By")

    # Using st.markdown for a more structured, styled list
    st.markdown("""
    <ul style="list-style-type: none; padding-left: 0;">
        <li style="font-size: 15px; margin-bottom: 10px;">👨‍💻 <strong>Abhishek Prabhu</strong></li>
        <li style="font-size: 15px; margin-bottom: 10px;">👨‍💻 <strong>Anjor Rane</strong></li>
        <li style="font-size: 15px; margin-bottom: 10px;">👨‍💻 <strong>Chetan Chimankare</strong></li>
        <li style="font-size: 15px; margin-bottom: 10px;">👨‍💻 <strong>Harsh Shirole</strong></li>
    </ul>
    """, unsafe_allow_html=True)
# "Feedback Analysis" section
elif selected == '🔍 Feedback Analysis':
    # CSS to position the logo at the top-right corner
    st.markdown(
        """
        <style>
        .logo {
            position: absolute;
            top: 0;
            right: 0;
            width: 150px;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Display the logo
    st.image("_1523354169_521_amazon-preview (1).jpg", use_column_width=False, width=150)

    # Main title and feedback analysis section
    st.markdown("<h1 class='main-title'>Feedback Analysis</h1>", unsafe_allow_html=True)

    # Review Text Input
    st.markdown("<p class='sub-title'>Enter your review text below:</p>", unsafe_allow_html=True)
    review_text = st.text_area("", height=200, placeholder="Type your review here...")

    # Button to Analyze Feedback
    if st.button("Analyze Feedback"):
        if review_text:
            sentiment_score = analyze_sentiment(review_text)

            if sentiment_score is not None:
                scale_score = map_polarity_to_scale(sentiment_score)

                if sentiment_score > 0:
                    st.success(
                        f"The review is predicted to be **Positive** with a sentiment score of {sentiment_score:.1f}")
                elif sentiment_score < 0:
                    st.error(
                        f"The review is predicted to be **Negative** with a sentiment score of {sentiment_score:.1f}")
                else:
                    st.warning(
                        f"The review is predicted to be **Neutral** with a sentiment score of {sentiment_score:.1f}")
                st.markdown(f"Feedback Rating (on a scale of 1-5): **{scale_score}**")
                st.markdown(f"Emotion: {get_emoji_for_score(scale_score)}")

                # Prepare data for Altair chart with all scores from 1 to 5
                score_values = [1, 2, 3, 4, 5]
                sentiment_values = [0] * 5  # Default to 0 for all scores
                sentiment_values[scale_score - 1] = sentiment_score  # Set the sentiment score for the given score

                data = pd.DataFrame({
                    'Score': score_values,
                    'Sentiment': sentiment_values
                })

                # Altair bar chart: X-axis is 1 to 5 score, Y-axis is sentiment score
                chart = alt.Chart(data).mark_bar().encode(
                    x=alt.X('Score:O', title='Rating Score (1-5)'),  # Discrete values for scores
                    y=alt.Y('Sentiment:Q', title='Sentiment Score')
                ).properties(
                    width=500,
                    height=300,
                    title="Sentiment Analysis: Score vs Sentiment"
                )

                # Display the Altair chart
                st.altair_chart(chart, use_container_width=True)
            else:
                st.error("An error occurred during sentiment analysis.")
        else:
            st.error("Please enter a review to analyze.")
elif selected == '📊 Dashboard Analysis':
    # CSS to position the logo at the top-right corner
    st.markdown(
        """
        <style>
        .logo {
            position: absolute;
            top: 0;
            right: 0;
            width: 150px;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Display the logo
    st.image("_1523354169_521_amazon-preview (1).jpg", use_column_width=False, width=150)

    # Main title and dashboard analysis section
    st.markdown("<h1>Dashboard Analysis</h1>", unsafe_allow_html=True)

    # Initialize session state for sentiment data if not already done
    if 'sentiment_data' not in st.session_state:
        st.session_state.sentiment_data = {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "total_score": 0,
            "scale_score": 0
        }

    # Review Text Input for Dashboard
    st.markdown("<p>Enter your review text below:</p>", unsafe_allow_html=True)
    dashboard_review_text = st.text_area("", height=200, placeholder="Type your review here...")

    # Button to Analyze Feedback for Dashboard
    if st.button("Analyze Feedback"):
        if dashboard_review_text:
            sentiment_score = analyze_sentiment(dashboard_review_text)

            if sentiment_score is not None:
                scale_score = map_polarity_to_scale(sentiment_score)

                # Update session state based on sentiment score
                if sentiment_score > 0:
                    st.session_state.sentiment_data["positive"] += 1
                elif sentiment_score < 0:
                    st.session_state.sentiment_data["negative"] += 1
                else:
                    st.session_state.sentiment_data["neutral"] += 1

                # Update the total score and scale score
                st.session_state.sentiment_data["total_score"] += sentiment_score
                st.session_state.sentiment_data["scale_score"] = scale_score

                # Display the result
                sentiment_icon = "✅" if sentiment_score > 0 else "❌" if sentiment_score < 0 else "⚪"
                st.success(
                    f"{sentiment_icon} The review is predicted to be **{'Positive' if sentiment_score > 0 else 'Negative' if sentiment_score < 0 else 'Neutral'}**")
            else:
                st.error("An error occurred during sentiment analysis.")
        else:
            st.error("Please enter a review to analyze.")

    # Dashboard Panel
    st.markdown("<h2>Dashboard Metrics</h2>", unsafe_allow_html=True)
    with st.container():
        # Style for panel
        st.markdown("""  
                        <div style='padding: 20px; border-radius: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);'>
                            <h3 style='text-align: center; color: #000000'>Feedback Analysis Overview</h3>
                            <div style='display: flex; justify-content: space-between; padding: 20px;'>
                                <div style='text-align: center; flex: 1; margin-right: 10px;'>
                                    <h4 style='color: #4CAF50;'>Positive Reviews</h4>
                                    <h2 style='color: #4CAF50; font-weight: bold;'>{}</h2>
                                </div>
                                <div style='text-align: center; flex: 1; margin-right: 10px;'>
                                    <h4 style='color: #f44336;'>Negative Reviews</h4>
                                    <h2 style='color: #f44336; font-weight: bold;'>{}</h2>
                                </div>
                                <div style='text-align: center; flex: 1;'>
                                    <h4 style='color: #FFC107;'>Neutral Reviews</h4>
                                    <h2 style='color: #FFC107; font-weight: bold;'>{}</h2>
                                </div>
                            </div>
                            <hr style='border: 1px solid #e0e0e0;'>
                            <h4 style='color: #000000;'>Total Sentiment Score</h4>
                            <h2 style='color: #000000; font-weight: bold;'>{:.2f}</h2>
                            <h4 style='color: #000000;'>Average Score </h4>
                            <h2 style='color: #000000; font-weight: bold;'>{:.2f}</h2>
                        </div>
            """.format(
            st.session_state.sentiment_data["positive"],
            st.session_state.sentiment_data["negative"],
            st.session_state.sentiment_data["neutral"],
            st.session_state.sentiment_data['total_score'],
            st.session_state.sentiment_data['scale_score']
        ), unsafe_allow_html=True)


# New "BI Analysis" section for embedding Power BI dashboard
elif selected == '📈 BI Analysis':
    st.image("_1523354169_521_amazon-preview (1).jpg", use_column_width=False, width=150)
    st.markdown("<h1 class='main-title'>BI Analysis</h1>", unsafe_allow_html=True)

    # Replace this URL with the actual Power BI Embed URL
    power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=8a7e812d-dace-410b-87bc-9eff0e06cf83&autoAuth=true&ctid=7f28ae11-cd2a-4b23-9922-bfbaab2422fd"

    st.markdown(
        f"""
        <iframe title="Feedback Dash" width="1200" height="800" src="https://app.powerbi.com/reportEmbed?reportId=8a7e812d-dace-410b-87bc-9eff0e06cf83&autoAuth=true&ctid=7f28ae11-cd2a-4b23-9922-bfbaab2422fd" frameborder="0" allowFullScreen="true"></iframe>
        """,
        unsafe_allow_html=True
    )

