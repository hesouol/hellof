import os
import tempfile

from pyspark.sql import SparkSession

RECIPE_COLUMNS = ('cookTime', 'datePublished', 'description', 'image', 'ingredients', 'name', 'prepTime', 'recipeYield',
                  'url')
SPARK = SparkSession.builder.appName("IntegrationTests").getOrCreate()


def create_ingest_and_transform_folders():
    base_path = tempfile.mkdtemp()
    ingest_folder = "%s%singest" % (base_path, os.path.sep)
    transform_folder = "%s%stransform" % (base_path, os.path.sep)
    return ingest_folder, transform_folder

