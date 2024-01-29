# TL;DR

A simple Google Cloud Function _(Gen 2)_ that reads images from Google Cloud Storage and calls the Gemini API. This Cloud Function service works in conjunction with [Twilio](https://www.twilio.com/) to recieve images via mms. Twilio recieves messges and generates a webhook that triggers the Cloud Function.

Results are saved to [Firestore](https://firebase.google.com/docs/firestore) and displayed using a simple html page found [here](https://storage.googleapis.com/glc-demo-app-host/text.html).

# Gemini API

Gemini Pro Vision returns a text response from an input images and prompt. You can find more examples [here](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/sdk-for-gemini/gemini-sdk-overview-reference#generate-content-from-text-and-image).

# Setup

This project includes a yaml file for deployment to Google Cloud using Github Actions maintained here: https://github.com/google-github-actions/deploy-cloud-functions. The Github Action Workflow requires several _"Action Secrets"_ used to set environment variables during deployment. Set the following secrets in the repository before deployment.

| Action Secret | Value                                                          |
| ------------- | -------------------------------------------------------------- |
| GCP_SA_KEY    | Service Account Key used to authenticate GitHub to GCP Project |
| HMAC          | Salt key used to generate HMAC                                 |
