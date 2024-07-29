# Image Hub

The Image Hub is a web application designed to address the challenges of managing SARAO's growing image repository. This application provides a comprehensive solution for effective image management and controlled access.

## Key Goals

- Allow the general public (guest users) to browse and search a repository of low-resolution images.
- Enable guest users to request access to the original high-resolution versions of the images, providing a valid reason for the request.
- Empower SARAO administrators, such as department heads, to review and approve or disapprove these access requests based on the provided justification.

## Project Structure

IMAGESHUB
├── Back_End
│   ├── (backend files)
├── Front_End
│   ├── (frontend files)
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
└── README.md

## Image Hub Backend

The backend for the Image Hub application is built using Python and the Bottle framework. It provides various APIs for managing users, images, and requests.

### API Endpoints

#### User Endpoints
- `GET /api/get-users`: Get all users.
- `POST /api/sign-in`: Sign in a user.

#### Image Endpoints
- `POST /upload-image`: Upload an image.
- `GET /api/get-image/<filename>`: Get an image by filename.
- `GET /api/get-image-data/<id>`: Get image data by ID.
- `GET /api/get-images`: Get all images.

#### Request Endpoints
- `POST /api/post-request`: Post a new request.
- `GET /api/get-request-data/<id>`: Get request data by ID.
- `GET /api/get-requests`: Get all requests.
- `PUT /api/update-request`: Update a request.

## Front-End

The front-end of the Image Hub is built using Angular 16, providing a user-friendly interface for interacting with the application's features.

### Features
- User authentication (sign-in)
- Browse and search low-quality images
- View or request high-resolution image details
- Browse and search requests
- View request details and requested image

### Angular Components
- **SignInComponent**: Handles user sign-in functionality.
- **BrowseImagesComponent**: Displays a list of uploaded images.
- **ImageDetailsComponent**: Shows details of a selected image.
- **BrowseRequestsComponent**: Displays a list of user requests.
- **RequestDetailsComponent**: Provides details of a selected request.

### Angular Services
- **UserService**: Manages user-related operations, such as sign-in and user data.
- **ImageService**: Handles image-related operations, such as fetching and displaying images.
- **RequestService**: Manages request-related operations, such as fetching and displaying requests.

## Getting Started

To clone and run this project, follow these steps:

### Prerequisites

- Ensure you have [Docker](https://www.docker.com/) installed on your machine.
- Install Python and create a virtual environment for the backend.

### Clone the Repository

`git clone https://github.com/sanelehlabisa/ImagesHub`
`cd ImagesHub`
Set Up the Backend
Navigate to the Back_End folder:

`cd Back_End`
Create a Python virtual environment and activate it:

`python3 -m venv venv`
`source venv/bin/activate`  # On Windows use `venv\Scripts\activate`

Install the required packages:
`pip install -r requirements.txt`

Set Up the Front-End

Navigate to the Front_End folder:

`cd ../Front_End`
Install the required packages:

`npm install`
Running the Application with Docker
Return to the root directory of the project:

`cd ..`
Start the application using Docker Compose:

`docker-compose up`
This command will build the necessary containers and start the application.

Conclusion
The Image Hub provides a robust solution for managing SARAO's image repository, facilitating easy access and effective management. For any questions or contributions, feel free to reach out!