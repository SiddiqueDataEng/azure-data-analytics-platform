# Troubleshooting Guide

## Quick Fix - Try These Scripts in Order:

### 1. First, run diagnostics:
```
diagnose.bat
```
This will check your Python installation and required packages.

### 2. Try the basic version (no virtual environment):
```
basic-run.bat
```

### 3. Try the simple version (with virtual environment):
```
simple-run.bat
```

### 4. Test Flask installation:
```
python test-app.py
```

## Common Issues and Solutions:

### Issue 1: "Python not found"
**Solution:**
1. Install Python from https://python.org
2. Make sure to check "Add Python to PATH" during installation
3. Restart command prompt after installation

### Issue 2: "pip not found"
**Solution:**
```
python -m ensurepip --upgrade
```

### Issue 3: "Flask not found" or import errors
**Solution:**
```
pip install Flask pandas faker pyarrow
```

### Issue 4: "app.py not found"
**Solution:**
Make sure you're running the batch file from the `data-generator` folder:
```
cd data-generator
basic-run.bat
```

### Issue 5: "templates not found"
**Solution:**
Make sure the `templates` folder exists with `index.html` inside it.

### Issue 6: Port already in use
**Solution:**
1. Close any other Flask applications
2. Or change the port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000 to 5001
```

### Issue 7: Permission errors
**Solution:**
Run command prompt as Administrator

## Manual Setup (if batch files don't work):

1. **Open Command Prompt**
2. **Navigate to data-generator folder:**
   ```
   cd path\to\data-generator
   ```
3. **Install packages:**
   ```
   pip install Flask pandas faker pyarrow
   ```
4. **Create temp folder:**
   ```
   mkdir temp
   ```
5. **Run the app:**
   ```
   python app.py
   ```

## Verify Installation:

Run these commands one by one:
```
python --version
pip --version
python -c "import flask; print('Flask OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import faker; print('Faker OK')"
```

## Still Not Working?

1. **Check Python PATH:**
   ```
   where python
   ```

2. **Reinstall packages:**
   ```
   pip uninstall Flask pandas faker pyarrow
   pip install Flask pandas faker pyarrow
   ```

3. **Try without pyarrow (optional dependency):**
   ```
   pip install Flask pandas faker
   ```
   Then comment out pyarrow import in app.py

4. **Use Python directly:**
   ```
   python -m flask run
   ```

## Contact Support:
If none of these solutions work, please provide:
- Your Python version (`python --version`)
- Your operating system
- The exact error message you're seeing
- Output from `diagnose.bat`