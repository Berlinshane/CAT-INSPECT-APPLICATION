# CAT Inspect Application

## Overview

The CAT Inspect Application is a robust multilingual vehicle inspection recording tool designed to streamline and enhance the vehicle inspection process. Developed with a combination of HTML, CSS, JavaScript, Flask, and SQLite3, the application integrates AI-generated recommendation summaries and secure user authentication, providing a comprehensive solution for vehicle inspection management.

## Features

- **Multilingual Support**: The application supports multiple languages, offering a user-friendly experience tailored to different language preferences.
- **AI-Generated Recommendations**: Utilizes AI to provide insightful recommendations based on inspection data.
- **Secure User Authentication**: Ensures that user data is protected with secure login and authentication mechanisms.
- **Comprehensive Data Management**: Facilitates efficient management of inspection data, including photo attachments and PDF downloads.
- **Responsive Design**: Features a professional and responsive design to ensure a seamless experience across various devices.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask
- **Database**: SQLite3
- **APIs**: Cohere API, MyMemory API, DropBox API
- **AI**: AI-generated recommendation summaries

## Installation

To get started with the CAT Inspect Application, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/cat-inspect-application.git
   cd cat-inspect-application
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **Mac/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up the Database**

   ```bash
   python setup_database.py
   ```

6. **Run the Application**

   ```bash
   python app.py
   ```

   The application will be available at `http://127.0.0.1:5000/`.

## Usage

1. **Navigate to the Application URL**: Open your web browser and go to `http://127.0.0.1:5000/`.
2. **Log In**: Use the secure login credentials to access the application.
3. **Perform Inspections**: Use the form to input vehicle inspection data, including fields for rust, dents, engine oil condition, brake fluid condition, and more.
4. **View Recommendations**: AI-generated recommendations will be provided based on the inspection data.
5. **Download Reports**: Attach photos and download inspection reports in PDF format.

## Contributing

Contributions to the CAT Inspect Application are welcome! To contribute:

1. **Fork the Repository**
2. **Create a Feature Branch**
3. **Commit Your Changes**
4. **Push to the Feature Branch**
5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact:

- **Email**: berlinshane18@gmail.com
- **GitHub**: https://github.com/Berlinshane

---

Feel free to adjust the URLs, contact information, or any other details to fit your specific setup.
