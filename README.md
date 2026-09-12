# Process That Image

Process That Image is a lightweight web-based image processing application built with Streamlit. The application provides simple image processing features, including background removal, background replacement, and image upscaling. Background removal is performed using U²-NetP through rembg, while image upscaling uses the FSRCNN super-resolution model with OpenCV DNN.

The application is designed with a simple and responsive interface that can be accessed from both desktop and mobile devices.

## Overview

This project was developed as a personal image processing project to explore the implementation of lightweight computer vision and deep learning models in a web-based application.

The application combines background segmentation and image super-resolution into a single interface, allowing users to process images without requiring complex image editing software.

## Features

- Remove image backgrounds automatically.
- Generate transparent backgrounds.
- Replace backgrounds with a solid color.
- Replace backgrounds using a custom image.
- Upscale images by 2× or 4×.
- Preview original and processed images side by side.
- Display original and output image dimensions.
- Download processed images as PNG.
- Responsive interface for desktop and mobile devices.

## Technology Stack

- Python
- Streamlit
- Pillow
- NumPy
- OpenCV
- OpenCV DNN Super Resolution
- rembg
- U²-NetP
- FSRCNN

## Image Processing Models

### Background Removal

Background removal is performed using U²-NetP through the `rembg` library.

| Component    | Description             |
| ------------ | ----------------------- |
| Architecture | U²-NetP                 |
| Runtime      | ONNX Runtime            |
| Deployment   | rembg                   |
| Processing   | Background Segmentation |
| Platform     | CPU                     |

U²-NetP is a lightweight variant of the U²-Net architecture designed for salient object detection and suitable for image background removal with relatively low computational requirements.

### Image Upscaling

Image upscaling is performed using FSRCNN through OpenCV DNN Super Resolution.

| Component    | Description                 |
| ------------ | --------------------------- |
| Architecture | FSRCNN                      |
| Framework    | OpenCV DNN                  |
| Deployment   | OpenCV DNN Super Resolution |
| Scale        | 2× and 4×                   |
| Processing   | Image Super-Resolution      |
| Platform     | CPU                         |

The pretrained FSRCNN models are included in the `models/` directory.

## Author

**Daniel Abdillah Arif**

LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/daniel-abdillah-arif-538a76418/)

GitHub: [GitHub Profile](https://github.com/DanielAArif)
