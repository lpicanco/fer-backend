import argparse
from keras.models import load_model
import tensorflow as tf
from keras import backend as K
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io
from tensorflow.python.saved_model import signature_constants
from tensorflow.python.saved_model import tag_constants

OUTPUT_FOLDER= 'frozen'
OUTPUT_GRAPH = 'frozen_model.pb'

def export(input_file, output_dir):
    K.set_learning_phase(0)
    K.set_image_data_format('channels_last')

    model = load_model(input_file)

    sess = K.get_session()
    frozen_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), [node.op.name for node in model.outputs])    
    graph_io.write_graph(frozen_graph, OUTPUT_FOLDER, OUTPUT_GRAPH, as_text=False)

    builder = tf.saved_model.builder.SavedModelBuilder(output_dir)

    with tf.gfile.GFile("%s/%s" % (OUTPUT_FOLDER, OUTPUT_GRAPH), "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    sigs = {}
    with tf.Session(graph=tf.Graph()) as sess:
        tf.import_graph_def(graph_def, name="")
        g = tf.get_default_graph()
        inp = model.inputs[0]
        out = model.outputs[0]

        sigs[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY] = \
            tf.saved_model.signature_def_utils.predict_signature_def(
                {"input": inp}, {"outout": out})

        builder.add_meta_graph_and_variables(sess,
                                            [tag_constants.SERVING],
                                            signature_def_map=sigs)
        builder.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The keras model file.")
    parser.add_argument("output_dir", help="The directory to save the exported model.")
    args = parser.parse_args()
    export(args.input_file, args.output_dir)