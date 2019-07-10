# Nanomine Testing
*TL;DR To write a custom test file, look at* `test_L102.py` *and* `test_L168.py` *as templates and modify as needed*

* The autoparser currently allows for automatic testing of the following categories:
  * PNC Present
  * Authors
  * Keywords
  * DOI Number
  * Language
  * Journal Volume
  * Matrix Chemical Names
  * Matrix Chemical Trade Names
  * Filler Chemical Names
  * Filler Chemical Trade Names
  * Devices
  * Temperatures
  * Material Properties Combined (ensuring properties are properly associated)
  * Filler Processing (Basic, needs to be expanded)
* This list will be expanded as new automated tests are developed

* The autoparser and all actual testing code are in `ingest_tester.py`

* Batch testing can be accomplished with `test_runner.py`
  * Run from whyis directory, `python apps/nanomine-graph/tests/test_runner.py <Number of tests to run> <--scramble>`
    * Can specify how many tests to run and if they should be selected randomly
    * Not giving a number will run tests for all files
  * Uses `test_auto.py` as a template, replacing <FILENAME HERE> with the target file
  * Outputs std-err to `/apps/nanomine-graph/tests/output.txt` to allow investigation of failed tests

* To write custom tests for particular files, create a new class and import from one of the following:
  * `test_template.IngestTestSetup` if you only want the setup and do not want to run all the automatic tests
  * `test_template.IngestTestTests` if you want to inherit all the automatic tests in addition to any custom tests
* Tests are executed with `/apps/whyis/venv/bin/python /apps/whyis/manage.py test --test=desired_test`, substituting `desired_test` with the test you wish to run omitting the file

## Potentially Missing Properties
* dielectricRealPermittivity