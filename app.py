from flask import Flask, render_template
import pandas as pd
import boto3, io, json
 
app = Flask(__name__)
 
# ---- S3 Configuration ----------------------------------------
S3_BUCKET = "devops2-endterm-rudra"
S3_KEY    = "u.user"
REGION    = "ap-south-1"
 
 
def fetch_dataframe():
    """Download u.user from S3 and return as a pandas DataFrame."""
    s3 = boto3.client("s3", region_name=REGION)
    obj = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    raw = obj["Body"].read().decode("utf-8")
    df  = pd.read_csv(
        io.StringIO(raw), sep="|",
        names=["user_id", "age", "gender", "occupation", "zip_code"]
    )
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    return df
 
 
@app.route("/")
def index():
    df = fetch_dataframe()
 
    # 1. Total users
    total_users = len(df)
 
    # 2. Age distribution (6 bands)
    bins   = [0, 18, 25, 35, 45, 55, 120]
    labels = ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    age_dist = df["age_group"].value_counts().sort_index()
    age_labels = [str(k) for k in age_dist.index]
    age_values = [int(v) for v in age_dist.values]
 
    # 3. Occupation grouping (top 15)
    occ = df["occupation"].value_counts().head(15)
    occ_labels = list(occ.index)
    occ_values = [int(v) for v in occ.values]
 
    # Extra stats
    avg_age      = round(float(df["age"].mean()), 1)
    male_count   = int((df["gender"] == "M").sum())
    female_count = int((df["gender"] == "F").sum())
    top_occ      = occ_labels[0] if occ_labels else "N/A"
 
    return render_template(
        "index.html",
        total_users  = total_users,
        avg_age      = avg_age,
        top_occ      = top_occ.capitalize(),
        male_count   = male_count,
        female_count = female_count,
        age_labels   = json.dumps(age_labels),
        age_values   = json.dumps(age_values),
        occ_labels   = json.dumps(occ_labels),
        occ_values   = json.dumps(occ_values),
        occ_table    = list(zip(occ_labels, occ_values)),
    )
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
