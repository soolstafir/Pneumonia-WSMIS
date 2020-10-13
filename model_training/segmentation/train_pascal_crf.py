import yaml
import torch
import numpy as np
import os

from model_training.common.trainer import Trainer
from model_training.common.datasets import PascalCRFSegmentationDataset
from model_training.common.augmentations import get_transforms

np.random.seed(0)
torch.manual_seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

with open(
    os.path.join(os.path.dirname(__file__), "config", "pascal_crf.yaml")
) as config_file:
    config = yaml.full_load(config_file)

train_transform = get_transforms(config["train"]["transform"])
val_transform = get_transforms(config["val"]["transform"])

train_ds = PascalCRFSegmentationDataset(
    config["train"]["path"],
    transform=train_transform,
    image_set="train",
    masks_folder=config["train"]["masks"],
    scale_factor=config["crf"]["scale_factor"],
)
val_ds = PascalCRFSegmentationDataset(
    config["val"]["path"],
    transform=val_transform,
    image_set="validation",
    masks_folder=config["val"]["masks"],
    scale_factor=config["crf"]["scale_factor"],
)

train_dl = torch.utils.data.DataLoader(
    train_ds, batch_size=config["batch_size"], shuffle=True, num_workers=12
)
val_dl = torch.utils.data.DataLoader(
    val_ds, batch_size=config["batch_size"], shuffle=True, num_workers=12
)

trainer = Trainer(config, train_dl, val_dl)
trainer.train()
