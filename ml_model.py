from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib
import os
import boto3
from botocore.exceptions import NoCredentialsError
import config
import pandas as pd

class MLModel:
    def __init__(self, cloud_storage=False, cloud_bucket=None):
        self.model = RandomForestClassifier()
        self.is_trained = False
        self.cloud_storage = cloud_storage
        self.cloud_bucket = cloud_bucket

        # For local saving/loading
        self.local_model_path = 'models/ml_model.pkl'

    def train(self, data, labels):
        """Train the model with given data and labels"""
        self.model.fit(data, labels)
        self.is_trained = True
        self.save_model()

    def predict(self, data):
        """Make predictions based on the trained model"""
        if not self.is_trained:
            return 0  # Return neutral prediction if model isn't trained
        return self.model.predict_proba(np.array([data]))[0][1]  # Confidence score for 'buy' class

    def save_model(self):
        """Save the model locally and optionally to cloud storage"""
        if self.cloud_storage:
            self.save_model_to_cloud()
        else:
            self.save_model_locally()

    def save_model_locally(self):
        """Save the trained model locally as a .pkl file"""
        joblib.dump(self.model, self.local_model_path)
        print(f"Model saved locally at {self.local_model_path}")

    def save_model_to_cloud(self):
        """Save the trained model to AWS S3"""
        try:
            # Initialize S3 client
            s3 = boto3.client('s3')
            model_data = joblib.dumps(self.model)
            s3.put_object(Bucket=self.cloud_bucket, Key='models/ml_model.pkl', Body=model_data)
            print(f"Model saved to S3 at s3://{self.cloud_bucket}/models/ml_model.pkl")
        except NoCredentialsError:
            print("Credentials not available. Please configure AWS CLI.")
        except Exception as e:
            print(f"Error saving model to S3: {e}")

    def load_model(self, from_cloud=False):
        """Load the model from local or cloud storage"""
        if from_cloud:
            return self.load_model_from_cloud()
        else:
            return self.load_model_locally()

    def load_model_locally(self):
        """Load the model from local storage"""
        if os.path.exists(self.local_model_path):
            self.model = joblib.load(self.local_model_path)
            self.is_trained = True
            print(f"Model loaded locally from {self.local_model_path}")
        else:
            print("No local model found.")
            self.is_trained = False
        return self.model

    def load_model_from_cloud(self):
        """Load the model from cloud storage"""
        try:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=self.cloud_bucket, Key='models/ml_model.pkl')
            model_data = response['Body'].read()
            self.model = joblib.loads(model_data)
            self.is_trained = True
            print(f"Model loaded from S3 at s3://{self.cloud_bucket}/models/ml_model.pkl")
        except Exception as e:
            print(f"Error loading model from S3: {e}")
            self.is_trained = False
        return self.model

    def get_features(self, data):
        """Process and return features for the model"""
        features = [
            data['rsi'],
            data['macd'],
            data['signal'],
            data['ema'],
            data['volume']
        ]
        return features
