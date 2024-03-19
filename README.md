# fastapi-docker-deploy
Practice repo for dockerizing a fastapi app with a database connection

## Goals

This repo exists so I can practice creating a simple fastapi application, dockerize it, and deploy it to a cloud provider.

## Rough in-order TODO

- [X] Create a FastAPI app with only static routes.
- [X] Create a Dockerfile that runs the FastAPI app
- [X] Get the Dockerfile Deployed in the cloud
        - Perhaps outside the scope of this repo
- [X] Add a database to the FastAPI app
- [X] Have the local app docker container communicate to a local db
- [X] Figure out how to deploy the app and connect it to an existing DB
- [X] Connect local api to local meilisearch instance
- [ ] Connect deployed API to GCP compute engine running meilisearch


## Steps to build image and put it in GCP Artifact Registry

This section will detail how to configure your GCP account and github to give the github workflow `gcp-upload.yaml` the opportunity to work correctly. This really exists so I can reproduce this quickly, without having to re-watch [the video](https://www.youtube.com/watch?v=6dLHcnlPi_U) I am plagarizing these steps from.

### In GCP 

1. Create a repository in Artifact Registry
    1. Give it a name
    2. Select Docker for the image type
    3. Select a region
2. Grant Access to an IAM role to push to registry
    1. Select the repository you created
    2. Show info panel
    3. in permissions, "add principal"
    4. In a seperate tab, navigate to "IAM & Admin" > "Service Accounts" and copy the email of the one you want.
    5. Back in the "add principal" page, give "Artifact Registry Writer" role to that email.
3. Create and Download Service Account Key
    1. Go to "IAM & Admin" > "Service Accounts"
    2. Select the service account you attached the permissions to
    3. Select "Keys" > "Add Key" > "Create new key" and select the JSON option
    4. Make sure it downloaded json to your device. If you lose this, then the key can't be updated on or added to any other services. You'll probably have to remove that key entirely and replace the private details everywhere it was used.
4. Get the setup URL
    1. Go to "Artifact Registry" > Your repo you just made > "Setup Instructions"
    2. Save that whole command for later

### In Github Repo
1. Add GCP Secrets to repo
    1. "Settings" > "Secrets and Variables" > "Actions" > "Repository secrets" and then click "Create repository secret"
    2. Name it "SERVICE_ACCOUNT_KEY" and paste in the contents of the JSON
2. In the workflow `gcp-upload.yaml` make sure you update these things:
    1. On line 13: your image name
    2. On lines 14 and 15: your GCP project details
    3. On line 31: that docker build points to the right directory where your Dockerfile sits
    4. On line 35: replace that gcloud command with the one from Step 4 of the "In GCP" section
    5. On lines 42-45: replace `<region>.pkg.dev` with the section from the command you saved from Step 4 of the "In GCP" section

## Steps to enable Cloud Run Deployment workflow

### In GCP

1. Set up permissions for workflow to run API
    1. Enable the Cloud Run Admin API in your GCP Project


### In `deploy.yaml` Workflow

1. Copy the same env variables from the `gcp-upload` workflow
    - Project ID
    - Repository Name
    - Image Name
2. Update Cloud run specification
    1. On line 27: update the service with the name you want for your cloud run service
    2. On line 28: fill in the image you want to use.
        - something like `us-central1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_ID/$IMAGE_NAME:latest`
