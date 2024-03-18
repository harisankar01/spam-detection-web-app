import packages.data_processor as dp
import streamlit as st 
import joblib
import pandas as pd
from extract_review import extract_review
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import rcParams
from analyze_data import compute_spamcity_with_exponential_smoothing

# Set TrueType font
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']

# Load the model
spam_clf = joblib.load(open('./models/spam_detector_model.pkl','rb'))

# Load vectorizer
vectorizer = joblib.load(open('./vectors/vectorizer.pickle', 'rb'))

### MAIN FUNCTION ###
def main(title = "Spam detection App".upper()):
    # st.markdown("<h1 style='text-align: center; font-size: 65px; color: #4682B4;'>{}</h1>".format(title), 
    # unsafe_allow_html=True)
    st.image("./images/message-image.jpg")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    with st.expander("Enter your product link: 😀"):
        text_message = st.text_input("Please enter your product link")
        if st.button("Predict"):
            review_data = pd.DataFrame(extract_review(text_message))
            if not review_data.empty: 
                styled_df = review_data.style.apply(color_rows, axis=1)
                st.write(styled_df, unsafe_allow_html=True)
                plt.figure(figsize=(8, 6))
                review_data['rating'].value_counts().sort_index().plot(kind='bar', color='skyblue')
                plt.xlabel('Rating')
                plt.ylabel('Count')
                plt.title('Distribution of Ratings')
                st.pyplot()

                # Word Cloud of Reviews
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(review_data['content']))
                plt.figure(figsize=(10, 6))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title('Word Cloud of Reviews')
                st.pyplot()

                # Pie Chart of Verified vs. Non-Verified Reviews
                plt.figure(figsize=(6, 6))
                review_data['is_verified'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightgreen'])
                plt.title('Proportion of Verified vs. Non-Verified Reviews')
                st.pyplot()

                # Histogram of Review Lengths
                plt.figure(figsize=(8, 6))
                review_data['review_length'] = review_data['content'].apply(len)
                plt.hist(review_data['review_length'], bins=20, color='lightcoral')
                plt.xlabel('Review Length')
                plt.ylabel('Frequency')
                plt.title('Histogram of Review Lengths')
                st.pyplot()

                # Stacked Bar Chart of Positive vs. Negative Reviews
                positive_reviews = review_data[review_data['rating'] >= 4].groupby('product_attributes').size()
                negative_reviews = review_data[review_data['rating'] < 4].groupby('product_attributes').size()
                positive_reviews.name = 'Positive Reviews'
                negative_reviews.name = 'Negative Reviews'
                review_comparison = pd.concat([positive_reviews, negative_reviews], axis=1).fillna(0)
                review_comparison.plot(kind='bar', stacked=True, figsize=(10, 6))
                plt.xlabel('Product Attributes')
                plt.ylabel('Count')
                plt.title('Positive vs. Negative Reviews by Product Attributes')
                st.pyplot()

                overall_spamcity_values = compute_spamcity_with_exponential_smoothing(data, 5, 0.2)

                for reviewer_id, spamcity in overall_spamcity_values.items():
                    print(f"Reviewer {reviewer_id}: Overall Spamcity = {spamcity}")
            else:
                st.success("Product don't exisits")

def color_rows(row):
    content = [row["content"]]  
    prediction = spam_clf.predict(vectorizer.transform(content))
    if prediction == 0:
        return ['background-color: yellow']*len(row)
    else:
        return ['background-color: red']*len(row)


if __name__ == "__main__":
    main()