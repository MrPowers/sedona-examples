from pyspark.sql import SparkSession
from sedona.spark import *
from .sedona import sedona
from sedona.sql.st_predicates import ST_DWithin
from sedona.sql.st_constructors import ST_Point
from pyspark.sql.functions import col, lit
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    FloatType,
)
from pathlib import Path


def test_st_dwithin():
    city_schema = StructType(
        [
            StructField("city_name", StringType()),
            StructField("long", FloatType()),
            StructField("lat", FloatType()),
        ]
    )
    schema = StructType(
        [
            StructField("left_point", city_schema),
            StructField("right_point", city_schema),
        ]
    )
    seattle_long = -122.335167
    seattle_lat = 47.608013
    new_york_long = -73.935242
    new_york_lat = 40.730610
    sydney_long = 151.2
    sydney_lat = -33.9
    df = sedona.createDataFrame(
        [
            (
                ("seattle", seattle_long, seattle_lat),
                ("new_york", new_york_long, new_york_lat),
            ),
            (
                ("seattle", seattle_long, seattle_lat),
                ("sydney", sydney_long, sydney_lat),
            ),
        ],
        schema,
    )
    print("@@@@@")
    df.show()
    print(df.schema)

    df.withColumn(
        "is_within_4k_km",
        ST_DWithin(
            ST_Point(col("left_point.long"), col("left_point.lat")),
            ST_Point(col("right_point.long"), col("right_point.lat")),
            lit(4000000),
            lit(True),
        ),
    ).show()


def test_st_areaspheroid():
    df = (
        sedona.read.format("csv")
        .option("delimiter", "\t")
        .option("header", "false")
        .load("data/county_small.tsv")
    )
    df.createOrReplaceTempView("some_counties")
    sql = """
    SELECT
        _c5 as county_name,
        ST_GeomFromWKT(_c0) as county_shape,
        ST_AreaSpheroid(county_shape) as county_area
    FROM some_counties
    """
    # sedona.sql(sql).show()


def test_st_centroid():
    df = (
        sedona.read.format("csv")
        .option("delimiter", "\t")
        .option("header", "false")
        .load("data/county_small.tsv")
    )
    df.createOrReplaceTempView("some_counties")
    sql = """
    SELECT
        _c5 as county_name,
        ST_GeomFromWKT(_c0) as county_shape,
        ST_Centroid(county_shape) as county_centriod 
    from some_counties
    """
    # sedona.sql(sql).show()


# def test_run_us_buildings():
#     home = Path.home()
#     sedona.read.format("geoparquet")\
#         .load(f"{home}/data/us-zip-codes.parquet")\
#         .createOrReplaceTempView("zipcodes")
#     sedona.read.format("geoparquet")\
#         .load(f"{home}/data/buildings")\
#         .createOrReplaceTempView("buildings")
#     sedona.sql(
#         """
#         SELECT zipcodes.zipcode, count(*) as numpoints
#         FROM zipcodes
#         JOIN buildings ON ST_Contains(zipcodes.geom, buildings.geom)
#         GROUP BY zipcodes.zipcode
#         """
#     ).write.mode("overwrite").csv(f"{home}/data/sedona/results.csv")
