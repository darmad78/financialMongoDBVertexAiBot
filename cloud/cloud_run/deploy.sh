#!/bin/bash
gcloud builds submit --tag gcr.io/[PROJECT_ID]/finance-assistant-backend
gcloud run deploy finance-assistant-backend --image gcr.io/[PROJECT_ID]/finance-assistant-backend --platform managed