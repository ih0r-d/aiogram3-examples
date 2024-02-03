## Telegram Bot examples using Aiogram v3

### Setting Up Environment

1. **Create a Virtual Environment**:
    ```shell
    python3 -m venv env 
    ```
   
2. **Activate the Virtual Environment**:
    ```shell
    source env/bin/activate 
    ```

3. **Upgrade pip**:
    ```shell
    pip install -U pip
    ```

### Installing Dependencies

1. **Install from requirements.txt**:
    ```shell
    pip install -r requirements.txt 
    ```

2. **Update Requirements File**:
    - After installing new packages, update `requirements.txt`:
        ```shell
        pip freeze > requirements.txt 
        ```

3. **Install Individual Packages**:
    - Install individual packages separately and update `requirements.txt`:
        ```shell
        pip install aiogram
        pip freeze >> requirements.txt 
        ```

### Note:
- Ensure that your virtual environment is activated before running any commands.
- Review `requirements.txt` periodically to keep track of package versions.
- For run on your side, please update `config.json`