import wandb
from lightning.pytorch import seed_everything

from model_fusion.train import setup_training
from model_fusion.datasets import DataModuleType
from model_fusion.models import ModelType
from model_fusion.config import BASE_DATA_DIR


def train_resnet18_mnist(min_epochs=20, max_epochs=100, batch_size=32, model_seed=42, data_seed=42, data_augmentation=False):
    seed_everything(model_seed, workers=True)
    datamodule_type = DataModuleType.MNIST
    datamodule_hparams = {'batch_size': batch_size, 'data_dir': BASE_DATA_DIR, 'seed': data_seed, 'data_augmentation': data_augmentation}

    model_type = ModelType.RESNET18
    model_hparams = {'num_classes': 10, 'num_channels': 1, 'bias': False}

    if batch_size == 128:
        lr = 0.01
    elif batch_size == 512:
        lr = 0.04
    else:
        lr = 0.1 * (batch_size / 32) * 0.25

    lightning_params = {'optimizer': 'sgd', 'lr': lr, 'momentum': 0.9, 'weight_decay': 0.0001, 'lr_scheduler': 'plateau', 'lr_decay_factor': 0.1, 'lr_monitor_metric': 'val_loss', 'model_seed': model_seed, 'data_seed': data_seed}

    wandb_tags = ['RESNET-18', 'MNIST', f"Batch size {batch_size}"]

    model, datamodule, trainer = setup_training(f'RESNET-18 MNIST B{batch_size}', model_type, model_hparams, lightning_params, datamodule_type, datamodule_hparams, min_epochs=min_epochs, max_epochs=max_epochs, wandb_tags=wandb_tags)

    datamodule.prepare_data()

    datamodule.setup('fit')
    trainer.fit(model, train_dataloaders=datamodule.train_dataloader(), val_dataloaders=datamodule.val_dataloader())

    datamodule.setup('test')
    trainer.test(model, dataloaders=datamodule.test_dataloader())

    wandb.finish()


if __name__ == '__main__':
    train_resnet18_mnist()
