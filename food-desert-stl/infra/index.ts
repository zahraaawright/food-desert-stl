import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

const region = gcp.config.region || "us-central1";

// Raw landing zone for API pulls before they're loaded into BigQuery
const rawBucket = new gcp.storage.Bucket("food-desert-raw", {
    location: region,
    forceDestroy: true,
    uniformBucketLevelAccess: true,
    lifecycleRules: [{
        condition: { age: 30 },
        action: { type: "Delete" },
    }],
});

// BigQuery dataset that dbt will read from and write models into
const dataset = new gcp.bigquery.Dataset("food_desert", {
    datasetId: "food_desert",
    location: region,
    description: "Raw and modeled data for the St. Louis food desert analysis",
});

export const rawBucketName = rawBucket.name;
export const bigQueryDatasetId = dataset.datasetId;
