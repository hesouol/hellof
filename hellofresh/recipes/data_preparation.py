import re

from pyspark.sql.functions import udf, to_date, col
from pyspark.sql.types import IntegerType


def _time_string_to_minutes(str_time: str) -> int:
    """
    :param str_time: String time as PT1H25M meaning 1 hour and 25 minutes.
    :return: time (int) in minutes (85 minutes in the example above).

    PT1H25M returns 85
    PT2H returns 120
    PT45M returns 45
    PT returns 0
    """
    total_time_in_minutes = 0
    hour_match = re.search('([0-9])*H', str_time)
    minute_match = re.search('([0-9])*M', str_time)
    if hour_match:
        total_time_in_minutes += 60 * int(hour_match.group()[:-1])
    if minute_match:
        total_time_in_minutes += int(minute_match.group()[:-1])
    return total_time_in_minutes


time_string_to_minutes_udf = udf(_time_string_to_minutes, IntegerType())


def prepare_df(recipes_df):
    return recipes_df.select(time_string_to_minutes_udf('cookTime').alias('cookTime'),
                             to_date(col('datePublished'), 'yyyy-MM-dd').alias('datePublished'),
                             'description',
                             'image',
                             'ingredients',
                             'name',
                             time_string_to_minutes_udf('prepTime').alias('prepTime'),
                             col('recipeYield').cast(IntegerType()).alias('recipeYield'),
                             'url'
                             )
