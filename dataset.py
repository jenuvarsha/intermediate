from azure.storage.blob import BlobServiceClient,BlobClient,ContainerClient
import pandas as pd

# Define your Azure storage account details
account_name = 'patientdatacts'
account_key = 'b7EtgSXLA3E9edXBvdm6c+ESTAT1pmUjRgY33+IKYLxyL/p7KaRVO9DpaKDoCGK0UMqAGS8BkE/f+ASttpPsFg=='
container_name = 'exported-data'
blob_name = 'exported-data/PatientClaimDatasetFinal.csv'

# Create a BlobServiceClient
blob_service_client = BlobServiceClient(account_url="https://patientdatacts.blob.core.windows.net", credential="b7EtgSXLA3E9edXBvdm6c+ESTAT1pmUjRgY33+IKYLxyL/p7KaRVO9DpaKDoCGK0UMqAGS8BkE/f+ASttpPsFg==")

# Get a client for the blob
blob_client = blob_service_client.get_blob_client(container="exported-data", blob="PatientClaimDatasetFinal.csv")

# Download the blob's content as a stream
stream = blob_client.download_blob().readall()
import io
df = pd.read_csv(io.BytesIO(stream))
print(df.head())