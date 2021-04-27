from pyspark.sql.functions import col, when, avg, lower


def compute_difficulty(_spark, dataframe):
    return dataframe.withColumn('totalCookingTime', col('cookTime') + col('prepTime')) \
                    .withColumn("difficulty", when(col('totalCookingTime') < 30, 'easy')
                                .when(col('totalCookingTime') > 60, 'hard')
                                .otherwise('medium')
                                )


def filter_beef_recipes(_spark, dataframe):
    return dataframe.where(lower(col("ingredients")).contains("beef"))


def calculate_average_time_per_difficulty(_spark, dataframe):
    return dataframe.groupBy(col('difficulty'))\
                           .agg(avg('totalCookingTime').alias('avg_total_cooking_time'))


def run(spark, input_dataset_path, transformed_dataset_path):
    input_df = spark.read.parquet(input_dataset_path)
    input_df.show()

    beef_filtered_df = filter_beef_recipes(spark, input_df)
    dataset_with_difficulty = compute_difficulty(spark, beef_filtered_df)
    final_df = calculate_average_time_per_difficulty(spark, dataset_with_difficulty)

    final_df.coalesce(1).write\
        .format("com.databricks.spark.csv")\
        .mode("overwrite")\
        .option("header", "true")\
        .save(transformed_dataset_path)
