FROM public.ecr.aws/amazonlinux/amazonlinux:latest

WORKDIR /app

RUN yum update -y
RUN yum install -y \
    python3 \
    python3-pip \
    python3-setuptools \
 && yum clean all \
 && rm -rf /var/cache/yum

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir --upgrade

COPY task.py .

ENTRYPOINT [ "python3", "/app/task.py" ]