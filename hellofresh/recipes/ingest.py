import logging

from hellofresh.recipes.data_preparation import prepare_df


def run(spark, ingest_path, transformation_path):
    logging.info(f'Reading text file from: {ingest_path}')
    input_df = spark.read.json(ingest_path)

    if input_df.rdd.isEmpty():
        raise ValueError(f'Empty dataframe on ingest path: {ingest_path}')

    transformation_df = prepare_df(input_df)
    logging.info(f'Writing parquet file to: {transformation_path}')
    transformation_df.write.mode('overwrite').parquet(transformation_path)



