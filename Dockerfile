FROM gw000/keras:2.1.4-py3-tf-cpu as builder
ARG FER_MODEL=cnnmodel-095-0.7827-0.7365.hdf5

COPY export_keras_model.py /work/
COPY ${FER_MODEL} /work/

WORKDIR /work
RUN pip3 install keras==2.2.4 && \
    python3 export_keras_model.py ${FER_MODEL} /exported_model 

FROM tensorflow/serving:1.13.0
LABEL maintainer="lpicanco@gmail.com"
COPY --from=builder /exported_model /models/model/1

ENTRYPOINT []
CMD ["/usr/bin/tf_serving_entrypoint.sh"]