"""Compute meanIOU."""

import os
import pickle

import jax.numpy as jnp

from data_loader import Loader
from train import UNet3D, normalize


def compute_iou(preds: jnp.ndarray, target: jnp.ndarray) -> jnp.ndarray:
    """Calculate meanIoU for a given batch.

    Args:
        preds (jnp.ndarray): Predictions from network
        target (jnp.ndarray): Labels

    Returns:
        jnp.ndarray: Mean Intersection over Union values
    """
    assert preds.shape == target.shape

    # TODO: implement iou.
    return jnp.array(0.0)


if __name__ == "__main__":
    keys = os.listdir("./data/gtexport/Test")
    model_path = "./weights/unet_499.pkl"  # Change this model path in case name differs
    input_shape = [128, 128, 21]
    mean = jnp.array([206.12558])
    std = jnp.array([164.74423])

    dataset = Loader(input_shape=input_shape, val_keys=keys)
    test_imgs = dataset.get_val(test=True)
    test_imgs, test_labels = test_imgs["images"], test_imgs["annotation"]
    batch_size = 2

    model = UNet3D()
    with open(model_path, "rb") as fp:
        net_state = pickle.load(fp)

    batched_imgs = jnp.split(test_imgs, len(test_imgs) // batch_size, axis=0)
    batched_labels = jnp.split(test_labels, len(test_imgs) // batch_size, axis=0)

    ious = []
    for batch_index in range(len(batched_imgs)):
        imgs, lbls = (
            normalize(batched_imgs[batch_index], mean, std),
            batched_labels[batch_index],
        )
        preds = model.apply(net_state, imgs)
        preds = jnp.argmax(preds, axis=-1)
        ious.append(compute_iou(preds, lbls))

    mean_iou = jnp.mean(jnp.array(ious))
    print(f"Mean IoU: {mean_iou}")
