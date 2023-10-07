
Build docker:
docker build -t dash: .

Run docker:
docker run --name dash_map -p 3000:3000 --env-file .env dash:1