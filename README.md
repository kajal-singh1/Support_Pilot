# SupportPilot – AI-Powered Customer Support Ticket Classification System

## 📌 Project Overview

SupportPilot is an AI-powered customer support ticket classification system designed to simplify and improve the ticket management process.

When a customer submits a support ticket, the system automatically predicts its category using Machine Learning, identifies its severity using rule-based logic, and assigns a priority based on severity and business impact.

The application also provides a dashboard where support teams can view, search, filter, and manage submitted tickets.

## 🎯 Objectives

- Automate customer support ticket classification.
- Reduce manual ticket categorization.
- Identify ticket severity and priority.
- Store and manage support tickets.
- Provide a dashboard for monitoring ticket status.

## ✨ Key Features

- **AI-Based Classification:** Automatically classifies tickets into Network, VPN, Password, Software, Hardware, and System categories.
- **Severity Detection:** Identifies Critical, High, Medium, and Low severity using predefined keyword-based rules.
- **Priority Assignment:** Assigns P1, P2, P3, or P4 based on severity and business impact.
- **Confidence Score:** Displays the machine learning model's estimated probability for its predicted category.
- **Ticket Management:** Stores submitted tickets in an SQLite database.
- **Dashboard Analytics:** Displays ticket statistics and category and priority distributions.
- **Search and Filters:** Helps support teams find tickets by relevant details.
- **Status Updates:** Allows tickets to be marked as Open, In Progress, or Resolved.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Framework | Flask |
| Machine Learning | Scikit-learn |
| Text Processing | TF-IDF Vectorization |
| Classification Algorithm | Logistic Regression |
| Data Processing | Pandas |
| Model Serialization | Joblib |
| Database | SQLite |
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Data Visualization | Chart.js |

## ⚙️ System Workflow

1. User submits a support ticket.
2. The ticket title and description are combined.
3. The trained machine learning model predicts the ticket category.
4. Rule-based logic identifies the ticket severity.
5. Priority is calculated using severity and business impact.
6. The system calculates the model confidence score.
7. Ticket details and predictions are stored in SQLite.
8. The dashboard displays the ticket and updated statistics.

## 🧠 Machine Learning Approach

The project uses a text classification pipeline consisting of:

- **TF-IDF Vectorization:** Converts ticket text into numerical features.
- **Logistic Regression:** Predicts the ticket category based on the extracted text features.
- **Rule-Based Severity Detection:** Uses predefined keywords to identify severity.
- **Priority Calculation:** Combines severity and business impact to assign priority.

Note: The initial training labels were generated using keyword-based rules. Therefore, the model's evaluation results measure agreement with those automatically generated labels and should not be interpreted as independently verified real-world accuracy.

## 📂 Project Structure

```text
SupportPilot/
│
├── app.py
├── database.py
├── severity_priority.py
├── prepare_training_data.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── data/
│   └── (Dataset and training files)
│
├── models/
│   └── ticket_classifier.pkl
│
├── templates/
│   └── index.html
│
├── static/
│
└── tests/
    ├── test_environment.py
    └── verify_database.py
```

Additional preprocessing and investigation scripts may also be included in the repository.

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/SupportPilot.git
cd SupportPilot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Prepare the Dataset and Model

Obtain the dataset separately and place the required CSV file in the `data/` directory.

Run the preprocessing and model-training scripts if you need to regenerate the training data and model.

The application requires the trained model file:

```text
models/ticket_classifier.pkl
```

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 🗄️ Database

SupportPilot uses SQLite to store ticket information, including:

- Employee details
- Ticket title and description
- Predicted category
- Severity
- Business impact
- Priority
- Confidence score
- Ticket status
- Creation timestamp

The database is created locally when the application runs.

## 🔮 Future Enhancements

- Improve classification using manually validated training data.
- Explore more advanced NLP and machine learning models.
- Improve severity prediction.
- Add email notifications for critical tickets.
- Introduce user authentication and role-based access.
- Deploy the application to a cloud platform.

## 👩‍💻 Author

Developed as part of the Infosys internship project.

**Project Name:** SupportPilot – AI-Powered Customer Support Ticket Classification System