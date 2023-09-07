# Image Code Generator using Flask

Welcome to the **Image Code Generator** – a user-friendly web application developed with Flask. This tool empowers users to effortlessly generate images with embedded codes sourced from a CSV file.

## Key Features

- **Upload**: Seamlessly upload an input image and a CSV file containing the desired codes.
- **Customization**: Tailor your image with options to adjust font size, font color, and code position.
- **Code Integration**: The CSV file is processed to generate images with the embedded codes.

## Prerequisites

Before you begin, ensure you have the following in place:

- **Python 3.x**
- **Flask Framework**
- **Pillow (PIL) Library**

## Installation

1. Clone this repository or download the ZIP file.
2. Install the necessary packages by executing the following command:
```
pip install Flask Pillow
```

## Usage

1. Launch the Flask application:
```
python app.py
```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Follow the on-screen instructions to upload your chosen input image and the accompanying CSV file. Customize font settings to match your preferences.

4. Click the "Process" button to initiate the generation of images with embedded codes.

5. Visit the "Result" page to review and download the newly generated images.

## Project Structure

The project directory consists of the following elements:

- `app.py`: The core Flask application file.
- `static/`: Houses static assets such as uploaded files and the resultant images.
- `templates/`: Contains HTML templates responsible for page rendering.

## Acknowledgments

This project is built upon the Flask web framework and utilizes the Pillow library for image manipulation.

## License

This project operates under the [MIT License](https://opensource.org/licenses/MIT).

- Develop by [Abdelrahman Nasr](test)
