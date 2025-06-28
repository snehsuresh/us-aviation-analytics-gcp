// Mismatch Analysis Summary in Scala (for Databricks)

// Import required functions
import org.apache.spark.sql.functions._

// Load the Spark table
val df = spark.table("workspace.default.mismatch_index_table")


// Carrier-Year Mismatch Summary
val carrierSummary = df
  .groupBy("CARRIER", "YEAR", "mismatch_bucket")
  .agg(count("*").alias("route_count"))
  .groupBy("CARRIER", "YEAR")
  .pivot("mismatch_bucket", Seq("Oversupplied", "Balanced", "Undersupplied"))
  .sum("route_count")
  .na.fill(0)

// Display sorted by Oversupplied
display(carrierSummary.orderBy(desc("Oversupplied")))


// Quarterly Mismatch Trend (All Carriers)
val timeTrend = df
  .groupBy("YEAR", "QUARTER", "mismatch_bucket")
  .agg(count("*").alias("count"))
  .groupBy("YEAR", "QUARTER")
  .pivot("mismatch_bucket", Seq("Oversupplied", "Balanced", "Undersupplied"))
  .sum("count")
  .na.fill(0)
  .orderBy("YEAR", "QUARTER")

display(timeTrend)



// Region + Distance Group Summary
val regionSummary = df
  .groupBy("REGION", "DISTANCE_GROUP", "mismatch_bucket")
  .agg(count("*").alias("route_count"))
  .groupBy("REGION", "DISTANCE_GROUP")
  .pivot("mismatch_bucket", Seq("Oversupplied", "Balanced", "Undersupplied"))
  .sum("route_count")
  .na.fill(0)
  .orderBy("REGION", "DISTANCE_GROUP")

display(regionSummary)


// Export Time Trend to CSV (Saved to DBFS)
timeTrend
  .coalesce(1) // Optional: write to a single file
  .write
  .option("header", "true")
  .csv("/dbfs/tmp/mismatch_summary.csv")

println("✅ CSV saved to /dbfs/tmp/mismatch_summary.csv")
