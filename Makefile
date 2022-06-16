export IMAGE_NAME=polygonio-news-sentiment-api

local-build:
	docker build . -t polygonio-news-sentiment-repo/$(IMAGE_NAME)

local-run:
	docker run --rm -p 8160:8160 polygonio-news-sentiment-repo/$(IMAGE_NAME)

gcp-auth:
#	gcloud components update
#	gcloud auth login
	gcloud config set project mlops-3
	gcloud auth configure-docker us-central1-docker.pkg.dev

gcp-build:
	docker build -t "us-central1-docker.pkg.dev/mlops-3/polygonio-news-sentiment-repo/$(IMAGE_NAME)" .

gcp-push:
	docker push us-central1-docker.pkg.dev/mlops-3/polygonio-news-sentiment-repo/$(IMAGE_NAME)

gcp-run:
	gcloud run deploy polygonio-news-sentiment-api \
  	--image us-central1-docker.pkg.dev/mlops-3/polygonio-news-sentiment-repo/$(IMAGE_NAME) \
  	--platform managed \
  	--region us-central1 \
  	--project mlops-3
