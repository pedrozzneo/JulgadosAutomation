# Project Documentation

## Overview
This project is designed to automate the process of generating PDFs from a web application using Selenium for web scraping. It consists of a backend that handles the logic for interacting with the web driver and a frontend that provides a user interface for input.

## Project Structure
```
TJ_Project
├── backend
│   ├── app.py          # Main application logic
│   ├── tests.py        # Unit tests for the application
│   └── __init__.py     # Marks the backend directory as a Python package
├── frontend
│   ├── index.html      # Main HTML file for user input
│   ├── renderer.js     # JavaScript logic for handling user interactions
│   └── styles.css      # Styles for the frontend application
├── dependencies
│   ├── package.json    # npm configuration file
│   └── package-lock.json # Locks the versions of dependencies
├── docs
│   └── README.md       # Documentation for the project
├── .gitignore          # Specifies files to ignore by Git
└── thingsThatCouldComeInHandy.txt # Notes and code snippets
```

## Setup Instructions
1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd TJ_Project
   ```

2. **Install Dependencies**
   Navigate to the `dependencies` directory and run:
   ```
   npm install
   ```

3. **Run the Application**
   - Start the backend server by running `app.py`.
   - Open `index.html` in a web browser to access the frontend.

## Usage
- Enter the required information in the form fields on the frontend.
- Click the "Generate PDF" button to initiate the PDF generation process.

## Testing
- Unit tests for the application can be found in `tests.py`. Run the tests to ensure the application functions as expected.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License.