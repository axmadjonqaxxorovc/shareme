# ShareMe

ShareMe is a simple and fast local network file sharing web application that allows you to upload files to your computer within your local network and easily download them on other devices like phones or tablets.

## Features

- **Local Network File Sharing**  
  Share files directly over your local network without the need for internet access.

- **Unique Session Folders**  
  Each upload is stored in a unique temporary folder for privacy and organization.

- **QR Code Download Link**  
  Automatically generates a QR code for quick access and easy sharing with other devices.

- **User-friendly Interface**  
  Simple and clean web interface to upload and download files quickly.

## For what?

ShareMe is designed to make file sharing between devices on the same local network easy, fast, and secure without needing the internet or cloud services.

It is perfect for:

- Quickly transferring files from your computer to phones, tablets, or other devices connected to the same Wi-Fi.
- Sharing large files without uploading them to external servers.
- Maintaining privacy by keeping all files within your local network.
- Providing a simple, user-friendly interface with QR code support for easy downloads.

In summary, ShareMe solves the problem of fast, private, and hassle-free file sharing within a local network.

## How It Works

1. Open the ShareMe web page on your computer connected to your local network.
2. Upload a file using the web interface.
3. Share the generated URL or scan the displayed QR code on your phone or other devices.
4. Download the file directly from your computer over the local network.

## Installation & Running

1. Clone the repository:
```
   git clone <repository-url>
   cd shareme
```

Install dependencies:

```
    pip install -r requirements.txt

```

Run the app:

```
    python router.py
    Open your browser and go to the printed local IP and port, for example:
    http://8.8.8.8:<random_port>
```
**Notes**
*Make sure your devices are connected to the same local network.*

*Uploaded files are temporarily stored and cleaned up when the app stops.*

*The QR code simplifies file access from mobile devices.*