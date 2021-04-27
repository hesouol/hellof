# HelloFresh - Recipes ETL

## Pre-requisites

* Python (3.9 or later)
* Pipenv
* Java (1.8 or later)

## Install all dependencies
```bash
pipenv install
```
## Run tests
### Run unit tests
```bash
pipenv run unit-test
```

### Run integration tests
```bash
pipenv run integration-test
```

## Create .egg package
```bash
pipenv run packager
```

## Use linter
```bash
pipenv run linter
```
## Jobs
### Recipes
At HelloFresh we have a big recipes archive that was created over the last 8 years. It is constantly being updated either by adding new recipes or by making changes to existing ones. We have a service that can dump archive in JSON format to selected s3 location. We are interested in tracking changes to see available recipes, their cooking time and difficulty level.


There are recipe files for this under `resources/recipes/*.json` with historical data.

#### Ingest
Reads `*.json` files and transforms it to `parquet` format, casting fields with the proper type.

##### Input
Historical recipes `*.json` files, this is a recipe example:
```json
{
	"name": "Creamy Cheese Grits with Chilies",
	"ingredients": "4-1/2 cups Water\n1/2 teaspoon Salt\n1 cup Grits (quick Or Regular)\n1/2 can (10 Ounce Can) Rotel (tomatoes And Chilies)\n1 can (4 Ounce Can) Chopped Green Chilies\n8 ounces, weight Monterey Jack Cheese, Grated\n4 ounces, weight Cream Cheese, Cut Into Cubes\n1/4 teaspoon Cayenne Pepper\n1/4 teaspoon Paprika\n Black Pepper To Taste\n1 whole Egg Beaten",
	"url": "http://thepioneerwoman.com/cooking/2010/10/creamy-cheese-grits-with-chilies/",
	"image": "http://static.thepioneerwoman.com/cooking/files/2010/10/5079611293_ff628b6e0c_z.jpg",
	"cookTime": "PT45M",
	"recipeYield": "8",
	"datePublished": "2010-10-14",
	"prepTime": "PT5M",
	"description": "I have a good, basic recipe for cheese grits in my cookbook, but last night I was feeling feisty.     I was cooking steaks. B..."
}
```
##### Output
`*.parquet` files applying the following:

1) `cookTime` and `prepTime` are converted from text to number (minutes)

2) `datePublished` and `recipeYield` are casted to date and number respectively.


##### Run the ingestion
Please make sure to package the code before submitting the spark job (`pipenv run packager`)
```bash
pipenv run spark-submit  
    --master local 
    --py-files dist/hellofresh-0.1.0-py3.9.egg 
    jobs/hellofresh_job.py
    INGEST 
    <INPUT_FILE_PATH> 
    <OUTPUT_PATH>
```

##### Example
```
pipenv run spark-submit --master local --py-files dist/hellofresh-0.1.0-py3.9.egg  jobs/hellofresh_job.py  INGEST resources/recipes resources/transformed/recipes
```

#### Recipe Difficulty Processing
This task is responsible for:
1) Extract only recipes that have beef as one of the ingredients.
2) Calculate average cooking time duration per difficulty level.
3) Persist dataset as CSV to the output folder.

##### Input
The `*.parquet` files ingested previously.

##### Outputs
The dataset have 2 columns: difficulty,avg_total_cooking_time.
Total cooking time duration = cookTime + prepTime

Criteria for levels based on total cook time duration:
```
    easy - less than 30 mins
    medium - between 30 and 60 mins
    hard - more than 60 mins.
```


##### Run Recipe Difficulty Calculation
```bash
pipenv run spark-submit 
    --master local 
    --py-files dist/hellofresh-0.1.0-py3.9.egg 
    jobs/hellofresh_job.py
    CALC 
    <INPUT_PATH> 
    <OUTPUT_PATH>
```

##### Example

```bash
pipenv run spark-submit --master local --py-files dist/hellofresh-0.1.0-py3.9.egg  jobs/hellofresh_job.py CALC resources/transformed/recipes resources/output/recipes
```

### Output
Recipes `CSV` File.
```csv
difficulty,avg_total_cooking_time
medium,45.0
hard,194.3913043478261
easy,19.625
```