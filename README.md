# DGJ2

# Project Setup

## Overview
This project requires a set of dependencies to be installed for proper execution. Follow the steps below to set up the project after cloning it from Git.

## Prerequisites
Make sure you have the following installed:
- Python (>=3.7)
- pip (Python package manager)
- (Optional) Virtual Environment for isolated dependency management

## Installation Steps

### 1. Clone the Repository
```sh
git clone <repository_url>
cd <repository_name>
```

### 2. (Optional) Create and Activate a Virtual Environment

#### On macOS/Linux:
```sh
python -m venv venv
source venv/bin/activate
```

#### On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Run the following command to install all required dependencies:
```sh
pip install -r requirements.txt
```

### 4. Verify Installation
Ensure dependencies are installed correctly by running:
```sh
pip list
```

## Running the Project
Run the project using:
```sh
python jagter.py
```

Input start date as 'dd-MM-yyyy' and Input end date as 'dd-MM-yyyy'

omraader.csv has to include a format of Name, Latitude, Longitude