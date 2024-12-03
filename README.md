# gitlab-scrolling-message

Use
---

1. Write your message in [the input file](data/message_raw.txt)

2. Encode the message by running:
    ```shell
    poetry run encode
    ```

3. Set the date for the day the message should start in [the constants file](src/lambda_func/constants.py)

4. Make an environment variable in github the same as the name defined in [the constants file](src/lambda_func/constants.py)
(currently "GITHUB_PERSONAL_ACCESS_TOKEN", but be sure to double check!)

5. Then zip and upload the contents of [src/lambda_func](src/lambda_func/) to a lambda function on AWS which is configured to run daily


Development
-----------
### Lint
```shell
bin/lint.ps1
```

### Testing
```shell
poetry run pytest
```
