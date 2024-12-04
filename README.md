# gitlab-scrolling-message

Want to display a message to the world in your github commit pixel grid?
This will auto-commit once a day to this repo in a way that will scroll your message (faintly) across the pixel grid.

Use
---

1. Write your message in [the input file](data/message_raw.txt)

2. Encode the message by running:
    ```shell
    poetry run encode
    ```

3. Set the date for the day the message should start in [the constants file](src/lambda_func/constants.py)

4. Setup an AWS lambda with a daily event trigger.

5. Make an environment variable in github the same as the name defined in [the constants file](src/lambda_func/constants.py)
(currently "GITHUB_PERSONAL_ACCESS_TOKEN", but be sure to double check!)

6. Zip and upload the contents of [src/lambda_func](src/lambda_func/) to the lambda function.

7. Fix the import statements in the lambda (i.e. remove `lambda_func.` from `from lambda_func.<module> import ...`)

8. Deploy and test.


Development
-----------
### TODO
- Improve the upload to AWS:
  - Enable uploading via command line
  - Remove the need for fixing the import statements once uploaded
- Add CI/CD pipeline in github running lint and tests that we already have
- Remove the constants from `constants.py` that aren't used by the lambda
- Test remaining untested functions in lambda_function.py

### Lint
```shell
bin/lint.ps1
```

### Testing
Ensure relevant ENV VARs are set

```shell
poetry run pytest
```
