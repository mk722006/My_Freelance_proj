import pandas as pd
import requests

# Function to download a file from a URL
def download_file(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded: {file_name}")
    else:
        print(f"Failed to download file: {file_name}")

# Function to process an Excel file
def process_excel_file(file_path):
    chunks_of_content = []  # Initialize an empty list to store chunks of content

    if file_path.endswith('.xlsx'):
        # Read all sheets of the Excel file
        sheets = pd.read_excel(file_path, sheet_name=None)
        
        for sheet_name, sheet_data in sheets.items():
            headers = sheet_data.columns.tolist()
            content = sheet_data.to_csv(index=False)  # Convert DataFrame to CSV string
            # Split content into smaller chunks
            content_chunks = split_into_chunks(content)
            chunks_of_content.extend(content_chunks)
    else:
        print(f"Unsupported file format: {file_path}")

    return chunks_of_content

# Function to split content into chunks of approximately 5000 tokens
def split_into_chunks(content):
    # Split the content into chunks of approximately 5000 tokens
    token_limit = 5000
    chunks = []
    current_chunk = ""
    current_chunk_token_count = 0

    for token in content.split():
        if current_chunk_token_count + len(token) > token_limit:
            chunks.append(current_chunk)
            current_chunk = ""
            current_chunk_token_count = 0
        current_chunk += token + " "
        current_chunk_token_count += len(token) + 1  # Add 1 for the space between tokens

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

# URLs of the Excel files
urls = [
    "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/58f8fd4ed1d842fe9a5cd9ad624b4ecc/download?&token=",
    "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/d1adf7185d824076a6ce58f7f43d282c/download?&token=",
    "https://sam.gov/api/prod/opps/v3/opportunities/resources/files/484ba48f24c24741b7ab5d0a889cc2ed/download?&token="
]

# File names
file_names = [
    "ATTACH_Attachment_1___Vendor_Submission_Form.xlsx",
    "ATTACH_Attachment_2___Pricing_Submission_Form.xlsx",
    "ATTACH_Attachment_4___ECAT_Item_Price_Import_Template.xlsx"
]

# Download and process each file
excel_file_paths = []

for url, file_name in zip(urls, file_names):
    download_file(url, file_name)
    excel_file_paths.append(file_name)

# Process the downloaded Excel files
all_chunks = []

for excel_file_path in excel_file_paths:
    chunks = process_excel_file(excel_file_path)
    print("===================", len(chunks))
    print(chunks[0])
    print("+=+++++++++++++++++")
    #print(chunks[1])
    print("===================")
    all_chunks.extend(chunks)

# Print the processed chunks
for chunk in all_chunks:
    print(chunk)
