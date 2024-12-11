# open-cascade-starter

## Install conda

https://www.anaconda.com/download/success

## Helpful Conda commands

```
conda config --add channels conda-forge
conda create --name=pyoccenv python=3.10
conda activate pyoccenv
conda install -c conda-forge pythonocc-core=7.8.1
conda deactivate
conda env remove --name pyoccenv
conda env list
```

## Run local

```
run_local.bat
```

## Deploy to Google Cloud

1. Install Docker CLI: https://www.docker.com/products/cli/

2. Install Google Cloud CLI: https://cloud.google.com/sdk/docs/install

3. Authenticate with Google Cloud and log in to project:

```
gcloud auth login
gcloud config set project [PROJECT_NAME]
```

4. Enable Google Cloud Run service:

```
gcloud services enable run.googleapis.com
```

5. Enable Artifact Registry and create repository: https://console.cloud.google.com/artifacts

```
gcloud services enable artifactregistry.googleapis.com
gcloud artifacts repositories create py-occ-server --repository-format=docker --location=us-central1
```

1. Build container image:

```
docker build -t py-occ-server .
```

6. Deploy on local: http://localhost:8000/

```
docker run --env-file .env -p 8000:8000 py-occ-server
```

7. Give build a tag to register with Google Artifact Registry

```
docker tag py-occ-server us-central1-docker.pkg.dev/[PROJECT_NAME]/py-occ-server/py-occ-server:latest
```

8. Push latest image to Google Artifact Registry

```
docker push us-central1-docker.pkg.dev/[PROJECT_NAME]/py-occ-server/py-occ-server:latest
```

9. Deploy latest image on Google Cloud Run with these settings (keep remaining default):

```
gcloud run deploy py-occ-server --image=[LOCATION]-docker.pkg.dev/[PROJECT_ID]/py-occ-server/py-occ-server:latest --platform=managed --region=us-central1 --allow-unauthenticated --port=8000
```

Once deployed, API will be accessible at the URL specified on the service details page: https://console.cloud.google.com/run/detail/us-central1/py-occ-server/

![image](https://github.com/user-attachments/assets/549f8500-0887-4603-bb6d-790b956380d6)

To modify your deployment settings, click the `Edit & Deploy New Version` button on the service details page. Here you can modify the deployment settings including adding your environmental variables as described below.

![image](https://github.com/user-attachments/assets/ef3081a4-55b6-47ad-aef0-69678fd55c3e)

![image](https://github.com/user-attachments/assets/369adf18-5c98-4658-b979-60b97af064cb)

## Environment variables

The following variables must be in the environment. For local development, place them in a file called `.env` in the root of the project.

```
S3_BUCKET_NAME=[the name of the S3 bucket to save generated geometry]
AWS_ACCESS_KEY_ID=[your aws key]
AWS_SECRET_ACCESS_KEY=[your key secret]
S3_REGION=[the region where the S3 bucket is hosted, ex. 'us-east-1']
```

When deploying to the cloud, specify the environment variables as part of the employment. For production environment, an additional variable is needed:

```
ENV=PROD
```
