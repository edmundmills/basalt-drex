from pathlib import Path
import time

import numpy as np
import matplotlib.pyplot as plt


class TrainingRun:
    def __init__(self, label, lr, epochs):
        self.name = f'{int(round(time.time()))}_{label}'
        self.lr = lr
        self.epochs = epochs
        self.losses = []
        self.update_frequency = 100
        self.timestamps = []

    def append_loss(self, loss):
        self.losses.append(loss)
        self.timestamps.append(time.time())

    def print_update(self, iter_count):
        if (iter_count % self.update_frequency) == 0:
            smoothed_loss = sum(
                self.losses[-self.update_frequency:-1])/self.update_frequency
            duration = self.timestamps[-1] - self.timestamps[-self.update_frequency]
            rate = self.update_frequency / duration
            print(
                f'Iteration {iter_count}. Loss: {smoothed_loss:.2f}, {rate:.2f} it/s')

    def smoothed_losses(self):
        smoothed_losses = []
        current_bucket = []
        for loss in self.losses:
            current_bucket.append(loss)
            if len(current_bucket) == self.update_frequency:
                smoothed_losses.append(sum(current_bucket)/len(current_bucket))
                current_bucket.clear()
        return smoothed_losses

    def save_data(self):
        save_path = Path('training_runs') / self.name
        save_path.mkdir(exist_ok=True)
        data = {'timestamps': self.timestamps,
                'losses': self.losses,
                'lr': self.lr,
                'epochs': self.epochs}
        np.save(file=save_path / 'data.npy', arr=np.array(data))
        fig = plt.figure()
        plt.ylabel('Loss')
        plt.xlabel(f'iterations (x{self.update_frequency})')
        plt.plot(self.smoothed_losses())
        plt.savefig(save_path / 'loss_plot.png')
