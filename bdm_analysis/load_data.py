from google.oauth2 import service_account
from google.cloud import bigquery
import os

def load_data_from_bigquery():
    """
    Loads data from BigQuery using GCP credentials.
    
    Returns:
        pd.DataFrame: The retrieved dataset.
    """
    try:
        key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        credentials = service_account.Credentials.from_service_account_file(key_path)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        
        query = """
        SELECT * FROM `edhec-business-manageme.luxurydata2502.price-monitoring-2022`
        WHERE brand = 'Panerai'
        """
        df = client.query(query).to_dataframe()
        
        if df.empty:
            print("⚠️ No data found for this query.")
        else:
            print("✅ Data successfully retrieved!")
        
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None
