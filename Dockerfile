# Python નું વર્ઝન સિલેક્ટ કરો
FROM python:3.10.9

# વર્કિંગ ડિરેક્ટરી સેટ કરો
WORKDIR /app

# Backend ના requirements કોપી કરો અને ઇન્સ્ટોલ કરો
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Backend નો બાકીનો કોડ કોપી કરો
COPY backend/ ./

# Hugging Face માટે 7860 પોર્ટ પર સર્વર ચાલુ કરો
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
