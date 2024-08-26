# data-ingestion-aws
Load data from multiple sources into AWS S3

## Project Setup Instructions

Follow these steps to set up and run the project:

1. ### Install Docker
   - Ensure that Docker is installed on your system. If not, follow the [Docker installation guide](https://docs.docker.com/get-docker/) to install it.

2. ### Set Up Minio
   - Launch a Minio container and ensure it is up and running.
   - Create an access key and secret key for authentication.

3. ### Start PostgreSQL Instance
   - Ensure a PostgreSQL instance is up and running. You can use Docker or any other method to start the database.

4. ### Configure Postman Mock Server
   - Set up a Postman mock server to simulate API endpoints. You can refer to the [Postman documentation](https://learning.postman.com/docs/designing-and-developing-your-api/mocking-data/setting-up-mock/) for more details.

5. ### Clone the Repository
   - Clone this repository to your local system:
     `git clone https://github.com/sagadevanmi/data-ingestion-aws.git`
   - Navigate to the cloned repository:
     `cd data-ingestion-aws`

6. ### Install Python Dependencies
   - Install the required Python packages using `pip`:
     `pip install -r requirements.txt`

7. ### Prepare Source Files
   - Ensure that the `SourceFiles` folder is present in the parent directory of this repository.

8. ### Create Archival Files Folder
   - Create an `ArchivalFiles` folder at the same directory level as this repository.

9. ### Update Configuration
   - Modify the `constants.py` file located in the `scripts` folder with your specific details:
     - Database connection details
     - Minio access key and secret key
     - Postman API details
