import datetime
import os
import requests
import json
import logging

import gcsfs
import uvicorn

import numpy as np
import pandas as pd

from fastapi import FastAPI, Response
from typing import Union
from logging.config import dictConfig
from src.log_config import log_config

dictConfig(log_config)
logger = logging.getLogger("polygonio-news-sentiment-logger")

app = FastAPI()

# Startup
@app.on_event("startup")
def load_data():
    # Load data from GCS
    fs = gcsfs.GCSFileSystem(project='mlops-3')
    gcs_path = "gs://polygonio-news-sentiment-test/data/polygonio_news_data.pkl"
    # Check if pickle file exists
    if fs.exists(gcs_path):
        global df_sentiment
        df_sentiment = pd.read_pickle(gcs_path)
    else:
        return {"message": "Sentiment API: No data available"}

@app.get("/")
def health():
    return {"message": "Sentiment API"}

@app.get("/v1/reference/sentiment")
def sentiment(
    published_utc: Union[str, None] = None,
    published_utc_gte: Union[str, None] = None,
    ticker: Union[str, None] = None
):
    if ticker and published_utc:
        return {"ticker": ticker, "published_utc": published_utc}
    if ticker and published_utc_gte:
        return {"ticker": ticker, "published_utc_gte": published_utc_gte}
    if published_utc:
        return {"published_utc": published_utc}
    if published_utc_gte:
        return {"published_utc": published_utc_gte}
    if ticker:
        ticker_index = []
        for idx, x in df_sentiment["tickers"].iteritems():
            if ticker in x:
                ticker_index.append(idx)

        df_ticker = df_sentiment.iloc[ticker_index]
        # Return ticker payload
        return Response(df_ticker.to_json(orient="records"), media_type="application/json")
    
    # Return the full payload
    return Response(df_sentiment.to_json(orient="records"), media_type="application/json")
