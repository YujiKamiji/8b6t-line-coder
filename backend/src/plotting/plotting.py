import matplotlib.pyplot as plt

class Plotting:
    @staticmethod
    def plot_8b6t(signal: str, save_path: str | None = None):
        symbol_to_level = {'+': 1, '0': 0, '-': -1}
        levels = [symbol_to_level[s] for s in signal]

        x = list(range(len(levels) + 1))
        y = [levels[0]] + levels

        plt.figure(figsize=(len(signal) / 10, 3))
        plt.step(x, y, where='post')
        plt.ylim(-1.5, 1.5)
        plt.yticks([-1, 0, 1], ['-V', '0', '+V'])
        plt.xlabel("Tempo")
        plt.ylabel("Tensão")
        plt.title("Sinal codificado 8B6T")
        plt.grid(True)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)
        else:
            plt.show()
