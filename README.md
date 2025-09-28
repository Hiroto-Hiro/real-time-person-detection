# 🎥 real-time-person-detection - Smart Surveillance Made Easy

## 📥 Download Now!
[![Download](https://img.shields.io/badge/Download-Now-blue.svg)](https://github.com/Hiroto-Hiro/real-time-person-detection/releases)

## 🌟 Overview
The **real-time-person-detection** project offers an AI-powered surveillance system using YOLOv8 for person detection. This system can send notifications through Telegram, keeping you informed about activity in real time. Whether you're watching over your home or office, this tool helps you monitor spaces effectively and securely.

## 🚀 Getting Started
This section will guide you through downloading and running the application on your computer. No programming skills are necessary.

### 1. System Requirements
- **Operating System:** Windows, macOS, or Linux
- **RAM:** Minimum 4 GB
- **Storage:** At least 1 GB of free space
- **Internet connection:** Required for initial setup

### 2. Prerequisites
Before downloading the application, ensure the following are installed on your computer:
- **Python** (version 3.7 or later)
- **Docker** (for container deployment)
- **Docker Compose** (for managing multi-container applications)

For a smooth installation, you can download Python from [python.org](https://www.python.org/downloads/) and follow the instructions for Docker and Docker Compose from their official websites.

## 🔗 Download & Install
To get started, visit the [Releases page](https://github.com/Hiroto-Hiro/real-time-person-detection/releases) to download the latest version of the application.

1. Click on the link above.
2. Find the version you want under the Releases section.
3. Download the appropriate file for your operating system. 

After downloading, here’s how to install and run the application:

### Running the Application
1. **For Docker Users:**
   - Open your terminal.
   - Navigate to the location of the downloaded Docker Compose file.
   - Run the command: 
     ```
     docker-compose up
     ```
   - This command will set up the application in a container.

2. **For Non-Docker Users:**
   - Unzip the downloaded file to a folder of your choice.
   - Open a terminal or command prompt in that folder.
   - Run the command:
     ```
     python app.py
     ```
   - The application will start, and you should see a message indicating it is running.

## ⚙️ Configuring the Application
Once the application is running, you may want to configure settings to suit your needs:

1. **Set Up Your IP Camera:**
   - Connect your IP camera to the same network as your computer.
   - Find the camera’s streaming URL. It usually follows a format like `http://<camera-ip>/video`.
   - Enter this URL in the application settings.

2. **Telegram Bot Setup:**
   - Create a new bot on Telegram using the BotFather.
   - Save the token provided by BotFather.
   - Input your bot token into the application's configuration file.

3. **Adjust Detection Settings:**
   - In the settings, you can adjust detection sensitivity, notification frequency, and other preferences.

## 📧 Get Support
If you encounter any issues or have questions, please open an issue on the GitHub repository. The community is here to help you.

## 🔑 Features
- Real-time person detection with YOLOv8.
- Instant notifications via Telegram.
- Supports multiple IP cameras simultaneously.
- User-friendly interface for quick setup.
- Lightweight and efficient system suitable for low-resource environments.

## 🌍 Topics Covered
- AI
- Computer Vision
- Machine Learning
- Real-time Monitoring
- Docker and Microservices

Feel free to explore, experiment, and make the most out of this surveillance system. Your safety and security are just a few clicks away.

## 📜 License
This project is licensed under the MIT License. You can use, modify, and distribute this software freely while giving credit to the original creators.