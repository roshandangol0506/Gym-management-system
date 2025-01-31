# 🏋️ Gym Management System

A web-based Gym Management System designed to streamline gym operations, manage trainers and customers, including payment tracking and facilitate payments via eSewa.

## 🚀 Features

Admin |||--- manages ---||| Trainer
Admin |||--- manages ---||| Customer
Admin |||--- tracks ---||| Payments
Admin |||--- sends email to ---||| Customer (for due payments)
Admin |||--- sendmessages ---||| Everyone (Trainer & Customer)

Trainer |||--- trains ---||| Customer
Trainer |||--- receives ---||| Leave Messages
Trainer |||--- participates in ---||| Events

Customer |||--- sends ---||| Leave Messages
Customer |||--- makes ---||| Payments (via eSewa)
Customer |||--- participates in ---||| Events

Admin |||--- organizes ---||| Events
Events |||--- have ---||| Participants (Customers)


### 👤 Admin
- Add, update, and delete trainers and customers (gym members)
- Track and manage customer gym fees
- Organize events and manage participants

### 💪 Trainer
- View assigned trainees
- Check leave messages from trainees

### 🏃 Customer (Gym Member)
- Log in to view payment statements and upcoming payment dates
- Send leave requests to trainers
- Make payments via eSewa

## 🛠️ Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Payment Gateway**: eSewa Integration

## 📸 Screenshots
![Screenshot (16)](https://github.com/user-attachments/assets/34acd136-ef30-484b-bed0-b7a7b2062f9d)
![Screenshot (17)](https://github.com/user-attachments/assets/8fd4b73b-97b4-49b5-be64-d151561af913)
![Screenshot (18)](https://github.com/user-attachments/assets/703485b9-e4c1-466c-9bd3-78e41416796b)
![Screenshot (19)](https://github.com/user-attachments/assets/791b3eaf-9cd1-45e4-85d3-59ca43779472)
![Screenshot (20)](https://github.com/user-attachments/assets/4d19e00f-5798-41e0-9f06-a7f5a225cc04)
![Screenshot (21)](https://github.com/user-attachments/assets/32f64718-b61c-4b7d-8ab4-b0f9a9b83b5f)


## 🔧 Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/Gym-management-system.git
