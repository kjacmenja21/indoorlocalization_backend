# Indoor Localization Backend

## Overview
The **Indoor Localization Backend** is part of a comprehensive solution designed to facilitate accurate indoor navigation. It supports asset tracking and data visualization by providing a robust backend infrastructure that powers web and mobile interfaces. This project includes features for managing assets, generating data reports, and integrating seamlessly with various front-end applications.

## Features
- **Asset Management**: Create, read, update, and delete (CRUD) operations for managing assets like devices or objects.
- **Data Reporting**: Offers tools for generating detailed reports and visualizations such as heatmaps, table summaries, and tail maps.
- **Scalability**: Built to handle multiple simultaneous requests, ensuring consistent performance under heavy loads.

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Python 3.11
- Poetry
For the backend to be able to work it requires a connection to a PostgreSQL database. It also requires a few environment variables to be set for it to work.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kjacmenja21/indoorlocalization_backend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd indoorlocalization_backend
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```

### Configuration
Update the configuration file with your environment settings:
- Database credentials
- API keys
- Other required parameters
Check `.example.env*` files to see possible keys.

### Running the Application
Start the backend server:
```bash
      python .\main.py
```

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
