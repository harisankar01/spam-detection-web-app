import requests
from pprint import pprint
import re

def extract_review(url):
    pattern = r"/dp/(.*?)/\?_"

    match = re.search(pattern, url)

    extracted_number = str(match.group(1))
    print(extracted_number)

    # Structure payload.
    payload = {
        'source': 'amazon_reviews',
        'domain': 'in',
        'query': extracted_number,
        'parse': True,
        'pages': 5
    }


    # Get response.
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('Harii', 'c9swBEUxT_6FPeV'),
        json=payload,
    )

    # Print prettified response to stdout.
    data = response.json()
    reviews =  data["results"]
    reviews_only = []
    
    current_page=""
    
    for i in reviews:
        # Check if 'reviews' key exists in i["content"]
        if "reviews" in i["content"]:
            current_page = i["content"]["reviews"]
            for j in current_page:
                reviews_only.append(j)


    pprint(reviews_only)
    return reviews_only

extract_review("https://www.amazon.in/Real-Book-Estate-Robert-Kiyosaki/dp/1612680798/?_encoding=UTF8&pd_rd_w=YAjyM&content-id=amzn1.sym.721fe359-5b18-49d2-bb73-de80fe9d4a7b%3Aamzn1.symc.acc592a4-4352-4855-9385-357337847763&pf_rd_p=721fe359-5b18-49d2-bb73-de80fe9d4a7b&pf_rd_r=0H4VRE1VC0ZS1FPVCQRR&pd_rd_wg=6Z2cN&pd_rd_r=71d935fa-9db7-4eab-a65a-7eb26d64a63a&ref_=pd_gw_ci_mcx_mr_hp_d")