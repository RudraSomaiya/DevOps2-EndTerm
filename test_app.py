import pytest
 
def test_flask_importable():
    """Flask must be importable (Build stage dependency check)."""
    import flask
    assert flask.__version__ is not None
 
def test_pandas_importable():
    """pandas must be importable."""
    import pandas as pd
    assert pd.__version__ is not None
 
def test_boto3_importable():
    """boto3 must be importable."""
    import boto3
    assert boto3.__version__ is not None
 
def test_app_object_exists():
    """Flask app object must be created without errors."""
    from app import app
    assert app is not None
    assert app.name == "app"
 
def test_flask_testing_mode():
    """Flask test client must be configurable."""
    from app import app
    app.config["TESTING"] = True
    client = app.test_client()
    assert client is not None
