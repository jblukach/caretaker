FROM public.ecr.aws/lambda/python:latest
RUN yum -y update && yum clean all
COPY cinsscore.py requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["cinsscore.handler"]