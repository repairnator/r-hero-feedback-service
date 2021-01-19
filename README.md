# R-hero-feedback-service

This repository contains the code for a simple web service that receives data generated from the [R-Hero PR feedback template](https://github.com/eclipse/repairnator/blob/master/src/repairnator-pipeline/src/main/resources/R-Hero-PR-text.MD).

Upon request, it connects to an Azure storage account, and stores the received data in a table. The request goes through a Recaptcha validation first.

## Dependencies

Install dependencies with `pip -i requirements.txt`

## Run

Setup the enviroment variables in `run.sh` and execute it.
