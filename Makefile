format:
	- poetry run black --line-length=120 --target-version=py38 src

lint:
	- poetry run flake8 --max-line-length=120

deploy:
	- sam package --template-file sam-template.yml --s3-bucket report-parser-artifacts --output-template-file sam-output-template.yml
	- sam deploy --template-file sam-output-template.yml --stack-name reports-parser --capabilities CAPABILITY_IAM 