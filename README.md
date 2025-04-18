# NRL Try Scorer Prediction using Machine Learning
# Model Still Under Development

This project uses machine learning and neural networks (TensorFlow + Keras) to predict NRL try scorers based on past performance and team statistics. The pipeline includes data wrangling, feature engineering, model training, evaluation, and prediction visualization.

---

##Project Features

- End-to-end ML pipeline using real NRL data
- Data wrangling and feature extraction with Pandas
- One-hot encoding and normalization
- Neural network model with dropout and L2 regularization
- Binary classification for predicting player tries
- Visualization of predictions vs. actual outcomes

---

## 🧪 Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- TensorFlow / Keras
- Matplotlib

---

## 🚀 Getting Started

### 🔧 Prerequisites

Make sure you have Python 3.7+ installed on your system.

---

### Clone the Repository

```bash
git clone https://github.com/your-username/nrl-try-prediction.git
cd nrl-try-prediction

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate   # For macOS/Linux

# OR for Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

nrl-try-prediction/
├── Cleanned Data/             # Processed dataset
├── NRLSTATS_RAW_DATA/         # Raw CSV game data
├── functions/                 # Custom helper functions
├── prediction_model.py        # Main training script
├── wrangle_data.py            # Data processing script
├── README.md                  # This readme file
