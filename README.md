# Online Chat Messenger

## Overview
This repository contains three sample implementations of a local chat messenger system.  
The project was created to learn socket programming, TCP/UDP communication, Electron frontend integration, and JSON-based message exchange.

## Samples

### Sample 1: Basic TCP/UDP Socket Communication
Basic Python socket programs for understanding how clients and servers communicate locally.

### Sample 2: Local Chat Messenger
A simple local messenger using Python sockets.  
This sample focuses on sending and receiving messages between a client and a server.

### Sample 3: Electron + Python TCP/UDP Messenger
A desktop application built with Electron and Python.  
Users can create a room, join a room with a shared key, and send free messages

Sample 3 is the most advanced implementation in this repository.  
It combines an Electron desktop frontend with Python backend servers using both TCP and UDP communication.

This sample was designed to simulate how a real-time chat system works internally, including:

- Room creation
- Room joining
- Real-time message exchange
- Message history retrieval
- Custom packet communication

---

# Architecture

```text
Electron Frontend
        ↓
renderer.js
        ↓
preload.js
        ↓
main.js (Electron IPC)
        ↓
TCP / UDP Socket Communication
        ↓
Python Backend Servers
```

The frontend and backend communicate using custom JSON packets.

---

# Protocol Design

The application separates responsibilities between TCP and UDP.

| Protocol | Purpose |
|---|---|
| TCP | Room creation and reliable communication |
| UDP | Room joining and real-time messaging |

This design was inspired by how modern communication systems separate reliable operations and fast lightweight communication.

---

# Features

## 1. Room Creation (TCP)

Users can create a room using:

- Room Name
- Password

The frontend automatically generates a UUID room key.

Example payload:

```json
{
  "operation": "CREATE",
  "room_name": "General",
  "password": "1234",
  "key": "generated-room-key",
  "users": []
}
```

The TCP server validates the request and stores room information locally.

---

## 2. Room Joining (UDP)

Users can join an existing room using:

- Shared Room Key
- Username

Example payload:

```json
{
  "operation": "JOIN",
  "key": "shared-room-key",
  "username": "Yu"
}
```

After joining successfully:

- Chat UI becomes visible
- User information is stored
- Message history is automatically loaded

---

## 3. Real-Time Messaging (UDP)

Messages are sent through UDP communication.

Example payload:

```json
{
  "operation": "MESSAGE",
  "key": "shared-room-key",
  "username": "Yu",
  "message": "Hello everyone"
}
```

The server stores the message and updates chat history.

---

## 4. Message History Retrieval

The client can request previous messages using:

```json
{
  "operation": "GET_HISTORY",
  "key": "shared-room-key"
}
```

The server filters messages by room key and returns the room history.

Example response:

```json
{
  "status": "success",
  "history": [
    {
      "username": "Yu",
      "message": "Hello"
    },
    {
      "username": "Alice",
      "message": "Hi"
    }
  ]
}
```

---

# Packet Structure

The application uses a custom packet structure.

Each packet contains:

- Header
- Payload

Example:

```json
{
  "header": {
    "json_size": 120,
    "operation_size": 7,
    "payload_size": 120
  },
  "payload": {
    "operation": "MESSAGE",
    "key": "room-key",
    "username": "Yu",
    "message": "Hello"
  }
}
```

This structure simulates how lower-level network systems separate metadata and actual payloads.

---

# Electron Frontend

The Electron frontend includes:

- Dynamic room operation UI
- Room creation popup
- UUID generation
- JSON preview visualization
- Chat interface
- Message history display
- Clipboard room-key sharing

The frontend communicates with Python backend servers through Electron IPC.

---

# Backend Design

The backend is separated into multiple responsibilities.

| File | Responsibility |
|---|---|
| server.py | TCP room creation |
| udp_server.py | UDP messaging and chat handling |
| validation.py | Input validation |
| room_service.py | Room storage management |

This separation improves maintainability and scalability.

---

# Networking Concepts Practiced

This project helped practice:

- TCP vs UDP communication
- Socket programming
- Client-server architecture
- Packet structure design
- JSON serialization
- Electron IPC communication
- Frontend/backend integration
- Real-time messaging systems

---

# Future Improvements

Possible future extensions include:

- Multi-user broadcasting
- Live message synchronization
- Database integration
- User authentication
- Persistent message storage
- Message encryption
- Voice chat
- WebSocket migration
- Channel-based rooms
- Online deployment
