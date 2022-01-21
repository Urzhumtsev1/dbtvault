---
id: y1cnt
name: The fixture registry
file_version: 1.0.2
app_version: 0.7.2-0
file_blobs:
  test/features/environment.py: 6749421573c62b931e1d2cc9f5748defc1f34938
  test/features/behave_fixtures.py: 8a295847eb45018e2cd21b84202c30e64b87f2c2
  test/features/staging/snowflake/snowflake_staging.feature: 3f28246bbaf19f88e7f1abab7fb00be9768ac93b
  test/features/staging/fixtures_staging.py: e4d82ab3b366fe838e891b7f6611f3179ad7c5cb
---

These fixtures are 'utility' fixtures and shared across all platforms.  
They add context variables/flags which the step implementations to perform certain logic
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/environment.py
```python
⬜ 16     from test.features.t_links import fixtures_t_link
⬜ 17     from test.features.xts import fixtures_xts
⬜ 18     
🟩 19     fixture_registry_utils = {
🟩 20         "fixture.enable_sha": enable_sha,
🟩 21         "fixture.enable_auto_end_date": enable_auto_end_date,
🟩 22         "fixture.enable_full_refresh": enable_full_refresh,
🟩 23         "fixture.disable_union": disable_union,
🟩 24         "fixture.disable_payload": disable_payload
🟩 25     }
⬜ 26     
⬜ 27     fixtures_registry = {
⬜ 28         "fixture.staging":
```

<br/>

e.g. `fixture.enable_full_refresh` provides a flag to the behave context which adds `--full-refresh` to the dbt command for a step.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/behave_fixtures.py
```python
⬜ 32         context.auto_end_date = True
⬜ 33     
⬜ 34     
🟩 35     @behave.fixture
🟩 36     def enable_full_refresh(context):
🟩 37         """
🟩 38         Indicate that a full refresh for a dbt run should be executed
🟩 39         """
🟩 40         context.full_refresh = True
⬜ 41     
⬜ 42     
⬜ 43     @behave.fixture
```

<br/>

This main fixtures registry contains a mapping for all possible fixtures, to their platform-specific implementations (functions)
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/environment.py
```python
⬜ 24         "fixture.disable_payload": disable_payload
⬜ 25     }
⬜ 26     
🟩 27     fixtures_registry = {
🟩 28         "fixture.staging":
🟩 29             {"snowflake": fixtures_staging.staging,
🟩 30              "bigquery": fixtures_staging.staging_bigquery,
🟩 31              "sqlserver": fixtures_staging.staging_sqlserver,
🟩 32              "databricks": ''},
⬜ 33     
⬜ 34         "fixture.staging_escaped":
⬜ 35             {"snowflake": fixtures_staging.staging_escaped,
```

<br/>

During development/execution of tests for a new platform, we may not have a platform specific implementation of a fixture yet. This is fine, just leave it as an empty string.  
  
When an implementation is added, this can then be updated.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/environment.py
```python
⬜ 77             {"snowflake": fixtures_link.single_source_comppk_link,
⬜ 78              "bigquery": fixtures_link.single_source_comppk_link_bigquery,
⬜ 79              "sqlserver": fixtures_link.single_source_comppk_link_sqlserver,
🟩 80              "databricks": ''},
⬜ 81     
⬜ 82         "fixture.multi_source_link":
⬜ 83             {"snowflake": fixtures_link.multi_source_link,
```

<br/>

The fixture annotation here is the same for all platforms, due to the mappings in the fixture regisry.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/staging/snowflake/snowflake_staging.feature
```cucumber
⬜ 1      Feature: [SF-STG] Staging
⬜ 2      
🟩 3        @fixture.staging
⬜ 4        Scenario: [SF-STG-01] Staging with derived, hashed, ranked and source columns.
⬜ 5          Given the STG_CUSTOMER table does not exist
⬜ 6          And the RAW_STAGE table contains data
```

<br/>

This is the snowflake implementation of the staging fixture, as defined in the fixture registry mapping.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/staging/fixtures_staging.py
```python
⬜ 1      from behave import fixture
⬜ 2      
⬜ 3      
🟩 4      @fixture
🟩 5      def staging(context):
🟩 6          """
🟩 7          Define the structures and metadata to load a hashed staging layer
🟩 8          """
🟩 9      
🟩 10         context.seed_config = {
🟩 11     
🟩 12             "STG_CUSTOMER": {
🟩 13                 "column_types": {
🟩 14                     "CUSTOMER_ID": "VARCHAR",
🟩 15                     "CUSTOMER_NAME": "VARCHAR",
🟩 16                     "CUSTOMER_DOB": "VARCHAR",
🟩 17                     "CUSTOMER_PHONE": "VARCHAR",
🟩 18                     "LOAD_DATE": "DATE",
🟩 19                     "SOURCE": "VARCHAR",
🟩 20                     "CUSTOMER_PK": "BINARY(16)",
🟩 21                     "HASHDIFF": "BINARY(16)",
🟩 22                     "EFFECTIVE_FROM": "DATE"
🟩 23                 }
🟩 24             },
🟩 25             "RAW_STAGE": {
🟩 26                 "column_types": {
🟩 27                     "CUSTOMER_ID": "VARCHAR",
🟩 28                     "CUSTOMER_NAME": "VARCHAR",
🟩 29                     "CUSTOMER_DOB": "VARCHAR",
🟩 30                     "CUSTOMER_PHONE": "VARCHAR",
🟩 31                     "LOAD_DATE": "DATE",
🟩 32                     "SOURCE": "VARCHAR"
🟩 33                 }
🟩 34             }
🟩 35         }
⬜ 36     
⬜ 37     
⬜ 38     @fixture
```

<br/>

The fixture registry works by merging the shared fixture registry mapping and the platform-specific mappings for each platform.

Aa simple dictionary comprehension filters the main fixture registry by platform.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/environment.py
```python
⬜ 183    
⬜ 184    }
⬜ 185    
🟩 186    fixture_registry_snowflake = {k: v['snowflake'] for k, v in fixtures_registry.items()}
🟩 187    fixture_registry_bigquery = {k: v['bigquery'] for k, v in fixtures_registry.items()}
🟩 188    fixture_registry_sqlserver = {k: v['sqlserver'] for k, v in fixtures_registry.items()}
🟩 189    fixture_registry_databricks = {k: v['databricks'] for k, v in fixtures_registry.items()}
🟩 190    
🟩 191    fixture_lookup = {
🟩 192        'snowflake': fixture_registry_utils | fixture_registry_snowflake,
🟩 193        'bigquery': fixture_registry_utils | fixture_registry_bigquery,
🟩 194        'sqlserver': fixture_registry_utils | fixture_registry_sqlserver,
🟩 195        'databricks': fixture_registry_utils | fixture_registry_databricks,
🟩 196    }
🟩 197    
⬜ 198    
⬜ 199    def before_all(context):
⬜ 200        """
```

<br/>

This is the magic that brings it all together. This function runs before every tag (e.g. @fixture)

It gets the current platform and fetches the fixtures for that platform, then selects the platform-specific implementation of the fixture if it finds a tag of the fixture type on a scenario.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 test/features/environment.py
```python
⬜ 233        dbtvault_generator.clean_test_schema_file()
⬜ 234    
⬜ 235    
🟩 236    def before_tag(context, tag):
🟩 237        tgt = env_utils.platform()
🟩 238    
🟩 239        if tgt in env_utils.AVAILABLE_PLATFORMS:
🟩 240            fixtures = fixture_lookup[tgt]
🟩 241            if tag.startswith("fixture."):
🟩 242                return use_fixture_by_tag(tag, context, fixtures)
🟩 243        else:
🟩 244            raise ValueError(f"Target must be set to one of: {', '.join(env_utils.AVAILABLE_PLATFORMS)}")
```

<br/>

This file was generated by Swimm. [Click here to view it in the app](https://app.swimm.io/repos/Z2l0aHViJTNBJTNBZGJ0dmF1bHQlM0ElM0FEYXRhdmF1bHQtVUs=/docs/y1cnt).