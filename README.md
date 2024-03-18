# Create An Awesome Streamlit App & Deploy it With Docker.      


## Run commands

```
pip install -r requirements.txt
```

```
streamlit run app.py
```

## API used

##### [Oxylab](https://oxylabs.io/)

Update username and password in `extract_review.py`

```
    response = requests.request(
        'POST',
        'https://realtime.oxylabs.io/v1/queries',
        auth=('username', 'pasword'),
        json=payload,
    )
```