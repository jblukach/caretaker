### 2.96.1 (build d2edb00) ###
FROM 070176467818.dkr.ecr.us-east-1.amazonaws.com/getpublicip:latest AS layer
FROM public.ecr.aws/lambda/python:latest
RUN yum -y update && yum clean all
### layer code ###
WORKDIR /opt
COPY --from=layer /opt/ .
### function code ###
WORKDIR /var/task
COPY abusech.py requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["abusech.handler"]