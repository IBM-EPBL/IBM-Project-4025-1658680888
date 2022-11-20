FROM python:3.10.6 
WORKDIR /app

ADD ./ Skill_Job_Recommendation_System

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000
CMD ["python","./app.py"]