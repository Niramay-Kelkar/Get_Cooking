# 
FROM python:3.8

# 
WORKDIR /app

# 
COPY ./requirements.txt ./requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
COPY . .

#
EXPOSE 8501

#
ENTRYPOINT ["streamlit", "run"]

# 
CMD ["landing.py"]
