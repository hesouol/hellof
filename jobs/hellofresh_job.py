import logging

import sys
from pyspark.sql import SparkSession

from hellofresh.recipes import ingest, difficulty_calculator

LOG_FILENAME = 'hellofresh.log'
APP_NAME = "HelloFresh: Recipes ETL"

if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    logging.info(sys.argv)

    if len(sys.argv) != 4:
        logging.error("Mode, Input source and output path are required")
        sys.exit(1)

    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    sc = spark.sparkContext
    app_name = sc.appName
    logging.info("Application Initialized: " + app_name)
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    if sys.argv[1] == 'INGEST':
        ingest.run(spark, input_path, output_path)
    elif sys.argv[1] == 'CALC':
        difficulty_calculator.run(spark, input_path, output_path)
    else:
        logging.error("Modes allowed are: CALC or INGEST")
        print("Modes allowed are: CALC or INGEST")
        sys.exit(1)

    logging.info("Application Done: " + spark.sparkContext.appName)
    spark.stop()