# Sedona Examples

This repo demos the functionality of Apache Sedona with PySpark and provides examples that can be easily run on your local machine.

You can run the test suite as follows: `uv run pytest tests`.

Make sure to install [uv](https://docs.astral.sh/uv/) on your machine to run the examples.  You should also have Java installed (Java 17 works well).

Here's how to run the test suite with the printed output displayed: `uv run pytest tests -s`.

## Demo Apache Sedona Capabilities

Suppose you have the following table with the longitude/latitude for the starting and ending locations of trips:

```
+----------+---------+---------+---------+-------+-------+
|start_city|start_lon|start_lat| end_city|end_lon|end_lat|
+----------+---------+---------+---------+-------+-------+
|  New York|    -74.0|     40.8|Sao Paulo|  -46.6|  -23.5|
| Sao Paulo|    -46.6|    -23.5|      Rio|  -43.2|  -22.9|
+----------+---------+---------+---------+-------+-------+
```

Use Sedona to compute the distance in meters for each trip:

```python
sql = """
SELECT 
    start_city,
    end_city,
    ST_DistanceSphere(
        ST_Point(start_lon, start_lat),
        ST_Point(end_lon, end_lat)) AS distance
FROM some_trips
"""
sedona.sql(sql).show()
```

Here's the result:

```

+----------+---------+-----------------+
|start_city| end_city|         distance|
+----------+---------+-----------------+
|  New York|Sao Paulo|7690115.108592422|
| Sao Paulo|      Rio|353827.8316554592|
+----------+---------+-----------------+
```

## Unit testing Apache Sedona

A unit test compares an actual result to an expected outcome.

Let's see how to unit test the `ST_Contains` function.

Start by invoking the function:

```python
sql = """
SELECT ST_Contains(
    ST_GeomFromWKT('POLYGON((175 150,20 40,50 60,125 100,175 150))'),
    ST_GeomFromWKT('POINT(174 149)')
) as result
"""
actual = sedona.sql(sql)
```

Now create an expected result and use chispa to confirm that the expected and actual DataFrames are the same:

```python
expected = sedona.createDataFrame([(False,)], ["result"])
chispa.assert_df_equality(actual, expected)
```

This library provides an easy way to invoke the Sedona functions on your local machine!

## Run Sedona in a Jupyter notebook

Create a kernel: `uv run ipython kernel install --user --name=sedonaexamples`.

Start the server: `uv run --with jupyter jupyter lab`.

You can open up the sample notebook and run the code.  Here is what it should look like:

![notebook sedona](https://github.com/MrPowers/sedona-examples/blob/main/images/sedona-notebook.png)
