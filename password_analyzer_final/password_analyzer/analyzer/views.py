from django.shortcuts import render
from django.contrib.auth.hashers import make_password  # for password hashing
from .models import Password  # assuming you have a Password model
import math
import re
from collections import Counter

# Create your views here.
def analyze_password(request):
    if request.method == 'POST':
        password = request.POST['password']

        # Analyze password strength
        entropy = calculate_entropy(password)

        analysis_results = []
        if len(password) < 8:
            analysis_results.append("Password should be at least 8 characters long.")
        if not re.search(r"[a-z]", password):
            analysis_results.append("Password should contain lowercase letters.")
        if not re.search(r"[A-Z]", password):
            analysis_results.append("Password should contain uppercase letters.")
        if not re.search(r"\d", password):
            analysis_results.append("Password should contain numbers.")
        if not re.search(r"[\W]", password):
            analysis_results.append("Password should contain special characters.")
        if re.search(r"(\w)\1{2,}", password):
            analysis_results.append("Password contains repeating characters.")
        if password.lower() in open("common_passwords.txt").read().splitlines():
            analysis_results.append("Password is a common password.")

        # Additional security (optional)
        # Check against a dictionary of leaked passwords
        # ... (implement if needed)

        # Store password securely in the database (optional)
        hashed_password = make_password(password)
        new_password = Password(password=hashed_password)  # assuming your model has a password field
        new_password.save()  # save the password (hashed)

        context = {'password': password, 'analysis_results': analysis_results}
        return render(request, 'analyzer/result.html', context)

    else:
        return render(request, 'analyzer/index.html')  # render the index page for GET requests


def calculate_entropy(password):
    char_counts = Counter(password)
    max_frequency = max(char_counts.values())
    entropy = len(password) * math.log2(len(set(password)))  # base-2 logarithm

    if max_frequency > len(password) / 2:
        entropy -= 0.5  # Adjust entropy for uneven distribution
    if re.search(r"(\w)\1{2,}", password):
        entropy -= 0.3  # Adjust entropy for repeating characters

    char_space = len(set(password))
    if char_space < 8:
        entropy -= 0.2  # Adjust entropy for smaller character space

    return entropy