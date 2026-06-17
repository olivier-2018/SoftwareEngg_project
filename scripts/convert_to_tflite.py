"""One-time conversion of SavedModel directories to .tflite.

Run locally with `tensorflow-cpu` installed (dev dependency group):
    uv run --extra dev python scripts/convert_to_tflite.py
"""
import pathlib
import tensorflow as tf
from tensorflow.python.saved_model import loader
from tensorflow.python.saved_model import tag_constants

ML_MODEL_DIR = pathlib.Path(__file__).resolve().parent.parent / "ML_model"

MODELS = [
    "audio_MNIST_v3-TF_v2.3.0.tf",
    "audio_MNIST_v3-TF_v2.7.0.tf",
]


def convert(saved_model_dir: pathlib.Path) -> pathlib.Path:
    """Convert a SavedModel directory to TFLite format.

    Uses low-level loader to skip optimizer state, then freezes the graph for conversion.
    """
    path = str(saved_model_dir)

    # Load only the serving graph (skips optimizer state like the runtime app does)
    sess = tf.compat.v1.Session()
    metagraph = loader.load(sess, [tag_constants.SERVING], path)
    signature = metagraph.signature_def[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY]

    # Get input/output tensor names from the signature
    input_key = list(signature.inputs.keys())[0]
    output_key = list(signature.outputs.keys())[0]
    input_tensor_name = signature.inputs[input_key].name
    output_tensor_name = signature.outputs[output_key].name

    # Get the actual tensor objects from the graph
    graph = sess.graph
    input_tensor = graph.get_tensor_by_name(input_tensor_name)
    output_tensor = graph.get_tensor_by_name(output_tensor_name)

    # Convert the session directly to TFLite using the v1 API
    converter = tf.compat.v1.lite.TFLiteConverter.from_session(
        sess,
        [input_tensor],
        [output_tensor]
    )
    converter.optimizations = []  # Disable optimizations to minimize numeric drift
    tflite_model = converter.convert()

    out_path = ML_MODEL_DIR / (saved_model_dir.name.removesuffix(".tf") + ".tflite")
    out_path.write_bytes(tflite_model)
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")

    sess.close()
    return out_path


if __name__ == "__main__":
    for name in MODELS:
        convert(ML_MODEL_DIR / name)
