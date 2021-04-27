from datetime import date
from hellofresh.recipes.ingest import run
from tests.integration import SPARK, create_ingest_and_transform_folders, RECIPE_COLUMNS


def test_ingest_with_data_preparation():
    """
        Integration test - data preparation and ingestion.
        Must apply conversion on columns cookTime and prepTime (from text to integer in minutes)
        Must cast publishedDate to date
        Must cast recipeYield to int
    """

    ingest_path, transform_path = create_ingest_and_transform_folders()

    #Writes source file
    SPARK.createDataFrame(
        [('PT20M', '2019-01-30', 'Boiled water', 'boiled_water.png', '1 cup of water', 'Delicious boiled water',
          'PT1H5M', '1', 'www.recipes.com/boiled_water.html')],
        RECIPE_COLUMNS
    ).write.json(ingest_path)

    #Execution
    run(SPARK, ingest_path, transform_path)
    actual = SPARK.read.parquet(transform_path)

    #Expected result
    expected = SPARK.createDataFrame(
        [(20, date(2019, 1, 30), 'Boiled water', 'boiled_water.png', '1 cup of water',
          'Delicious boiled water', 65, 1, 'www.recipes.com/boiled_water.html')],
        RECIPE_COLUMNS
    )

    assert actual.collect() == expected.collect()

