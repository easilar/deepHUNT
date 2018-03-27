import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def Plot_lossAccuracy( plots , tag, mplot):
    plt.style.use("ggplot")
    plt.figure()

    for c_plot in plots:
        N = c_plot["n"]
        plt.plot(np.arange(0, N), c_plot["plot"], c=c_plot["color"],label=c_plot["label"])

    plt.title("Training Loss and Accuracy on"+tag+"/Not "+tag)
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig(mplot+".png")
    plt.savefig(mplot+".pdf")
print mplot , " is saved"
