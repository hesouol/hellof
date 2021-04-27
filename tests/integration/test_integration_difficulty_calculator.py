import os
import tempfile
from datetime import date

from hellofresh.recipes.difficulty_calculator import compute_difficulty, filter_beef_recipes, \
    calculate_average_time_per_difficulty, run
from tests.integration import SPARK, RECIPE_COLUMNS, create_ingest_and_transform_folders


def test_should_generate_difficulty_column_and_calculate_total_cooking_time():
    """
    totalCookingTime = prepTime+cookTime
    difficulty = "easy < 30 min / hard > 60 min / medium: otherwise"
    """
    df = SPARK.createDataFrame(
        [
            (30, date(2019, 1, 30), 'r1', 'r1.png', '1 pinch of salt', 'r1', 1, 1, 'r1.html'),
            (0, date(2019, 1, 30), 'r2', 'r2.png', '1 cup of water ', 'r2', 2, 2, 'r2.html'),
            (60, date(2019, 1, 30), 'r3', 'r3.png', '1 grain of rice', 'r3', 3, 3, 'r3.html')
        ],
        RECIPE_COLUMNS
    )

    actual = compute_difficulty(SPARK, df)

    expected = SPARK.createDataFrame(
        [
            (30, date(2019, 1, 30), 'r1', 'r1.png', '1 pinch of salt', 'r1', 1, 1, 'r1.html', 31, 'medium'),
            (0, date(2019, 1, 30), 'r2', 'r2.png', '1 cup of water ', 'r2', 2, 2, 'r2.html', 2, 'easy'),
            (60, date(2019, 1, 30), 'r3', 'r3.png', '1 grain of rice', 'r3', 3, 3, 'r3.html', 63, 'hard')
        ],
        RECIPE_COLUMNS + ('totalCookingTime', 'difficulty')
    )

    assert expected.collect() == actual.collect()


def test_should_filter_beef_recipes():
    df = SPARK.createDataFrame(
        [
            (1, date(2019, 1, 30), 'r1', 'r1.png', '1 slice of plant based Beef', 'r1', 1, 1, 'r1.html'),
            (2, date(2019, 1, 30), 'r2', 'r2.png', '1 cup of water ', 'r2', 2, 2, 'r2.html')
        ],
        RECIPE_COLUMNS
    )

    actual = filter_beef_recipes(SPARK, df)

    expected = SPARK.createDataFrame(
        [
            (1, date(2019, 1, 30), 'r1', 'r1.png', '1 slice of plant based Beef', 'r1', 1, 1, 'r1.html'),
        ],
        RECIPE_COLUMNS
    )

    assert expected.collect() == actual.collect()


def test_should_calculate_average_time_per_difficulty():
    df = SPARK.createDataFrame(
        [
            (30, date(2019, 1, 30), 'r1', 'r1.png', '1 pinch of salt', 'r1', 1, 1, 'r1.html', 31, 'medium'),
            (60, date(2019, 1, 30), 'r2', 'r2.png', '1 cup of water ', 'r2', 2, 2, 'r2.html', 62, 'hard'),
            (60, date(2019, 1, 30), 'r3', 'r3.png', '1 grain of rice', 'r3', 3, 3, 'r3.html', 63, 'hard')
        ],
        RECIPE_COLUMNS + ('totalCookingTime', 'difficulty')
    )

    actual = calculate_average_time_per_difficulty(SPARK, df)

    expected = SPARK.createDataFrame(
        [
            ('medium', 31.0),
            ('hard', 62.5),
        ],
        ('difficulty', 'avg_total_cooking_time')
    )

    assert actual.collect() == expected.collect()


def test_run_difficulty_calculator():
    ingest_folder, transform_folder = create_ingest_and_transform_folders()

    df = SPARK.createDataFrame(
        [
            (1, date(2019, 1, 30), 'r1', 'r1.png', '1 slice of plant based beef', 'r1', 1, 1, 'r1.html'),
            (2, date(2019, 1, 30), 'r2', 'r2.png', '1 cup of water ', 'r2', 2, 2, 'r2.html')
        ],
        RECIPE_COLUMNS
    )

    df.write.parquet(ingest_folder, mode='overwrite')

    run(SPARK, ingest_folder, transform_folder)

    actual = SPARK.read\
                  .option("header", "true")\
                  .option("inferSchema", "true")\
                  .csv(transform_folder)

    expected = SPARK.createDataFrame(
        [('easy', 2.0)],
        ('difficulty', 'avg_total_cooking_time')
    )

    assert actual.collect() == expected.collect()


