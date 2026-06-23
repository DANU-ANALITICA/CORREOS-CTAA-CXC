Correr esto para crear archivos principales: 
touch main.py \
      requirements.txt \
      Dockerfile \
      .env \
      .gcloudignore && \
echo "✅ Estructura creada:" && ls -R

Intalar brew y gcloud. 
1. brew --version

2. si no la tienen; 
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

3. brew install --cask gcloud-cli

Una vez instalado esto: 

1. gcloud auth login
gcloud auth application-default login
Esto abrirlo en la cuenta donde se va a trabajar 

2. Confirmar que BigQuery te responde con una prueba rápida:
bashbq query --use_legacy_sql=false 'SELECT 1 AS prueba'
Si te devuelve un 1, ya tienes acceso y puedes empezar a probar el código en local.


Instalar librerias py: 

Colocar en entorno: 
python3 -m venv venv
source venv/bin/activate

Instalar: 
pip install google-cloud-bigquery pandas numpy db-dtypes pyarrow playwright python-dotenv

playwright install chromium

Para correr python de manera local: 
python main.py

