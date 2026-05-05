# E-Learning & Course Management Platform

A full-featured E-Learning / Coaching Management System built with **Python**, **Django**, and **SQLite**. This platform connects students, teachers, and administrators, allowing for seamless course browsing, wishlisting, purchasing, and management.

## 🚀 Features

- **Multi-Role Authentication System:**
  - **Admin:** Has a comprehensive dashboard to view total revenue, active users, all courses, and all successful orders.
  - **Manager (Teacher):** Can create, read, update, and delete their own courses. They can upload course thumbnails and instructor images.
  - **Customer (Student):** Can browse available courses, view detailed information, add courses to a wishlist, or proceed to checkout.
- **Payment Gateway Integration:** Secure checkout process using **Razorpay** API.
- **Secure Password Recovery:** Forgot password system utilizing email-based **OTP verification**.
- **User Profiles:** Users can update their profiles, including uploading and changing profile pictures.
- **Wishlist & Cart Management:** Allows students to keep track of interested courses and manage multiple items in their cart before payment.

## 🛠️ Technology Stack

- **Backend:** Python, Django
- **Database:** SQLite (default)
- **Payment Integration:** Razorpay API
- **Email Service:** SMTP (Gmail) for OTP and notifications

## ⚙️ Installation & Setup

1. **Navigate to the project directory** (where `manage.py` is located):
   ```bash
   cd path/to/myproject
   ```

2. **Activate the virtual environment** (if not already activated):
   ```bash
   # On Windows:
   ..\Scripts\activate
   ```

3. **Install required dependencies:**
   Ensure you have all the required libraries installed:
   ```bash
   pip install django razorpay
   ```

4. **Apply database migrations:**
   Run these commands to set up the database tables:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the local development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## 🔑 Key Configurations (settings.py)

For the email and payment systems to work correctly, ensure the following credentials in `myproject/settings.py` are properly configured:
- **Email Credentials:** `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` (use an App Password if using Gmail).
- **Razorpay API Keys:** `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`.

## 📂 Project Structure

- `myapp/` - Contains the main application logic, models (`User`, `Courses`, `Wishlist`, `Cart`), views, and URLs.
- `myproject/` - Contains core Django configuration settings and main URL routing.
- `media/` - Stores user-uploaded media like profile pictures and course thumbnails.
- `templates/` - Contains HTML files for the front-end interface.
- `db.sqlite3` - Local SQLite development database.
