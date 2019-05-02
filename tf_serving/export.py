import argparse
import tensorflow as tf
import keras
from keras.models import load_model
import os

def export(input_file, output_file):
    model = load_model(input_file)

    with tf.keras.backend.get_session() as sess:
        sess.run(tf.global_variables_initializer())
        tf.saved_model.simple_save(
            sess,
            output_file,
            inputs={'faces': model.input},
            outputs={'emotions': model.output})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The keras model file.")
    parser.add_argument(
        "output_file", help="The file to save the exported model.")
    args = parser.parse_args()
    export(args.input_file, args.output_file)
