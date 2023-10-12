### 2.100.0 (build e1b5c77) ###
FROM public.ecr.aws/forensicir/getpublicip:latest AS layer
FROM public.ecr.aws/lambda/python:latest
RUN yum -y update && yum clean all
### layer code ###
WORKDIR /opt
COPY --from=layer /opt/ .
### function code ###
WORKDIR /var/task
COPY nubinetwork.py requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["nubinetwork.handler"]