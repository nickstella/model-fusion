import wandb

from model_fusion.train import setup_training
from model_fusion.datasets import DataModuleType
from model_fusion.models import ModelType
from model_fusion.config import BASE_DATA_DIR


def train_vgg11_cifar100(min_epochs=0, max_epochs=1, batch_size=32):
    datamodule_type = DataModuleType.CIFAR100
    datamodule_hparams = {'batch_size': batch_size, 'data_dir': BASE_DATA_DIR}

    model_type = ModelType.VGG11
    model_hparams = {'num_classes': 100, 'num_channels': 3, 'bias': False}

    wandb_tags = ['VGG-11', 'CIFAR_100', f"Batch size {batch_size}"]

    model, datamodule, trainer = setup_training(f'VGG-11 CIFAR-100 B{batch_size}', model_type, model_hparams, datamodule_type, datamodule_hparams, min_epochs=min_epochs, max_epochs=max_epochs, wandb_tags=wandb_tags)

    datamodule.prepare_data()

    datamodule.setup('fit')
    trainer.fit(model, train_dataloaders=datamodule.train_dataloader(), val_dataloaders=datamodule.val_dataloader())

    datamodule.setup('test')
    trainer.test(model, dataloaders=datamodule.test_dataloader())

    wandb.finish()


if __name__ == '__main__':
    train_vgg11_cifar100()
