import os
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from keras.models import Model
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import linear_sum_assignment as linear_assignment
import seaborn as sns
from tqdm import tqdm
import pandas as pd
import config as cfg
from build_and_save_features import load_dataset
from metrics import acc, nmi
import nets
from mpl_toolkits.mplot3d import Axes3D
import umap
import predict
import random
import math
from scipy.spatial import Voronoi, voronoi_plot_2d


def plot_ae_tsne(encoder, ce_weights, figures, dataset, epoch=''):

    """
    parameters:
    - autoencoder,
    - encoder,
    - models_directory: directory containing the models,
    - figures: directory to save the plots
    - dataset: dataset on which to predict (train, val, test)

    Loads the model weigths from models directory, predicts model output,
    perfoms kmeans and tsne and plots result.
    """
    encoder.load_weights(ce_weights)
    kmeans = KMeans(n_clusters=cfg.n_clusters)
    features = encoder.predict(dataset)
    y_pred = kmeans.fit_predict(features)
    # centers3d = kmeans.cluster_centers_.astype(np.float32)
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter(features[:, 0], features[:, 1], features[:, 2], c=y_pred, cmap='brg')
    # ax.scatter(centers3d[0], centers3d[1], centers3d[2], c='black')
    # plt.savefig(os.path.join(figures, 'kmeans_ae_' + epoch))
    plt.figure()
    tsne = TSNE(n_components=2, perplexity=30, n_iter=1000)
    embedding = tsne.fit_transform(features)
    # centers2d = tsne.fit_transform(centers3d)
    plt.scatter(embedding[:, 0], embedding[:, 1], c=y_pred, s=20, cmap='brg')
    # plt.scatter(centers2d[0], centers2d[1], c='black')
    plt.savefig(os.path.join(figures, 'tsne_encoder_' + epoch))

    print('saved scatter plot ae')


def plot_ae_umap(encoder, ce_weights, figures, dataset, epoch=''):
    """
    parameters:
    - autoencoder,
    - encoder,
    - models_directory: directory containing the models,
    - figures: directory to save the plots
    - dataset: dataset on which to predict (train, val, test)

    Loads the model weigths from models directory, predicts model output,
    perfoms kmeans and tsne and plots result.
    """
    encoder.load_weights(ce_weights)
    kmeans = KMeans(n_clusters=cfg.n_clusters)
    features = encoder.predict(dataset)
    y_pred = kmeans.fit_predict(features)
    reducer = umap.UMAP()
    reducer.fit(features)
    embedding = reducer.transform(features)
    fig = plt.figure()
    plt.scatter(embedding[:, 0], embedding[:, 1], c=y_pred, s=20, cmap='brg')
    plt.savefig(os.path.join(figures, 'umap_encoder_' + epoch))
    print('saved scatter plot ae')


def plot_voronoi(centers, y_kmeans): 
    vor = Voronoi(centers) 
    voronoi_plot_2d(vor) 
    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=5, cmap='summer') 
    plt.show()


def plot_pretrain_metrics(file, save_dir):
    '''
    This function reads a csv file containing the pretraining metrics, plots
    them and saves an image in the figures folder.
    '''
    data = pd.read_csv(file)
    train_loss = data['train_loss']
    val_loss = data['val_loss']
    plt.figure()
    plt.plot(train_loss)
    plt.plot(val_loss)
    plt.title('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Training loss', 'Validation loss'])
    plt.savefig(os.path.join(save_dir, 'pretrain_metrics'))


def plot_train_metrics(file, save_dir):
    '''
    This function read a csv file containing the training metrics, plots them
    and saves an image in the figures folder.
    '''
    data = pd.read_csv(file)

    ite = data['iteration']
    train_loss = data['train_loss']
    val_loss = data['val_loss']
    clust_loss = data['clustering_loss']
    val_clust_loss = data['val_clustering_loss']
    rec_loss = data['reconstruction_loss']
    val_rec_loss = data['val_reconstruction_loss']
    train_acc = data['train_acc']
    val_acc = data['val_acc']
    train_nmi = data['train_nmi']
    val_nmi = data['val_nmi']
    train_ari = data['train_ari']
    val_ari = data['val_ari']

    # losses
    plt.figure(figsize=(30, 10))
    plt.subplot(1, 3, 1)
    x1 = ite
    y1 = train_loss
    y2 = val_loss
    plt.plot(x1, y1)
    plt.plot(x1, y2)
    plt.title('L')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'])

    plt.subplot(1, 3, 2)
    x1 = ite
    y1 = clust_loss
    y2 = val_clust_loss
    plt.plot(x1, y1)
    plt.plot(x1, y2)
    plt.title('Lc: clustering loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'])

    plt.subplot(1, 3, 3)
    x1 = ite
    y1 = rec_loss
    y2 = val_rec_loss
    plt.plot(x1, y1)
    plt.plot(x1, y2)
    plt.title('Lr: reconstruction loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'])
    plt.savefig(os.path.join(save_dir, 'train_val_loss'))

    # other metrics
    plt.figure(figsize=(30, 10))
    plt.subplot(1, 3, 1)
    x1 = ite
    y1 = train_acc
    y2 = val_acc
    plt.plot(x1, y1)
    plt.plot(x1, y2)
    plt.title('Accuracy')
    plt.ylabel('Acc')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'])

    plt.subplot(1, 3, 2)
    x1 = ite
    y1 = train_nmi
    y2 = val_nmi
    plt.plot(x1, y1)
    plt.plot(x1, y2)
    plt.title('NMI')
    plt.ylabel('NMI')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'])

    plt.subplot(1, 3, 3)
    x1 = ite
    y1 = train_ari
    y2 = val_ari
    plt.plot(x1, y1)
    plt.plot(x1, y2)
    plt.title('ARI')
    plt.ylabel('ARI')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'])
    plt.savefig(os.path.join(save_dir, 'train_val_acc_nmi_ari'))


def plot_confusion_matrix(y_true, y_pred, save_dir):
    matrix = confusion_matrix(
        [int(i) for i in y_true], y_pred)

    plt.figure()
    sns.heatmap(matrix, annot=True, fmt="d", annot_kws={"size": 20})
    plt.title("Confusion matrix")
    plt.ylabel('True label')
    plt.xlabel('Clustering label')
    plt.savefig(os.path.join(save_dir, 'confusion_matrix'))

    D = max(y_pred.max(), y_true.max()) + 1
    w = np.zeros((D, D), dtype=np.int64)
    # Confusion matrix.
    for i in range(y_pred.size):
        w[y_pred[i], y_true[i]] += 1
    ind = linear_assignment(-w)
    a = ind[0].tolist()
    b = ind[1].tolist()
    print(np.array([a, b]))


def plot_dataset():
    imgs = []
    for i in range(40):
        for scan in cfg.scans:
            n = random.randint(0, 50)
            imgs.append(predict.get_image(predict.get_list_per_type(cfg.train_directory, scan), n))
    random.shuffle(imgs)
    
    fig = plt.figure(frameon=False, figsize=(100,100))
    
    k = 10
    columns = k
    rows = k
    ax = []
    for i in range(1, columns*rows +1):
        img = imgs[i]
        ax.append(fig.add_subplot(rows, columns, i))        
        plt.imshow(img)
        plt.axis('off')
    
    plt.subplots_adjust(wspace=0.1, hspace=0, left=0, right=1, bottom=0, top=1)

    os.makedirs(os.path.join(cfg.figures, 'dataset'), exist_ok=True)
    plt.savefig(os.path.join(cfg.figures, 'dataset', 'scans.svg'))


def feature_map(scan, layer, depth, exp):
    # load image
    # load network aspc_29_CAE
    encoder = nets.encoder()
    encoder.load_weights(os.path.join(cfg.models, exp, 'ae', 'ce_weights'))
    model = Model(inputs=encoder.inputs, outputs=encoder.layers[layer].output)
    img = predict.get_image(predict.get_list_per_type(cfg.train_directory, scan), 1)
    img = np.expand_dims(img, axis=-1)
    img = np.expand_dims(img, axis=0)
    feature_maps = model.predict(img)

    fig = plt.figure(frameon=False, figsize=(30,30))

    # plot all
    square = math.sqrt(depth)
    if isinstance(square, float):
        square = int(square + 1)
    ix = 1
    for _ in range(square):
        for _ in range(square):
            # specify subplot and turn of axis
            ax = plt.subplot(square, square, ix)
            # plot filter channel in grayscale
            try:
                plt.imshow(feature_maps[0, :, :, ix-1])
            except:
                plt.imshow(np.zeros((feature_maps.shape[1], feature_maps.shape[1]), dtype=np.uint8))
            plt.axis('off')
            ix += 1
        plt.subplots_adjust(wspace=0.1, hspace=0, left=0, right=1, bottom=0, top=1)
    # show the figure
    
    os.makedirs(os.path.join(cfg.figures, cfg.exp, 'feature_maps'), exist_ok=True)
    plt.savefig(os.path.join(cfg.figures, cfg.exp, 'feature_maps', 'conv_layer_' + scan + '_' + str(layer) + '.png'))


if __name__ == "__main__":
    x_train, y_train = load_dataset('x_train.npy', 'y_train.npy')
    x_test, y_test = load_dataset('x_test.npy', 'y_test.npy')

    feature_map(scan=cfg.scans[0], exp='aspc_29_CAE', layer=1, depth=32)
    feature_map(scan=cfg.scans[1], exp='aspc_29_CAE', layer=1, depth=32)
    feature_map(scan=cfg.scans[2], exp='aspc_29_CAE', layer=1, depth=32)
    feature_map(scan=cfg.scans[0], exp='aspc_29_CAE', layer=2, depth=64)
    feature_map(scan=cfg.scans[1], exp='aspc_29_CAE', layer=2, depth=64)
    feature_map(scan=cfg.scans[2], exp='aspc_29_CAE', layer=2, depth=64)

    # autoencoder, encoder = nets.autoencoder(x_test)

    # plot_cae_kmeans( 
    #     encoder, 
    #     cfg.ce_weights, 
    #     os.path.join(cfg.figures, cfg.exp, 'cae'), 
    #     x_test
    # )
    
    # clustering_layer = ClusteringLayer(
    #     cfg.n_clusters, name='clustering')(encoder.output)
    # model = Model(
    #     inputs=encoder.input, outputs=[clustering_layer, cae.output])
    # model.compile(
    #     loss=['kld', 'mse'], loss_weights=[cfg.gamma, 1], optimizer='adam')

    # os.makedirs(os.path.join(cfg.figures, cfg.exp, 'cae'), exist_ok=True)
    # os.makedirs(os.path.join(cfg.figures, cfg.exp, 'dcec'), exist_ok=True)
    # # --- CAE ---
    # # plot tsne after kmean init
    # plot_cae_tnse(
    #     autoencoder=cae,
    #     encoder=encoder,
    #     models_directory=os.path.join(cfg.models, cfg.exp, 'cae'),
    #     figures=os.path.join(cfg.figures, cfg.exp, 'cae'),
    #     dataset=x_test
    # )

    # # plot pretrain metrics
    # plot_pretrain_metrics(
    #     file=os.path.join(cfg.tables, 'cae_train_metrics.csv'),
    #     save_dir=os.path.join(cfg.figures, cfg.exp, 'cae'),
    # )

    # # --- DCEC ---
    # # plot tsne dcec iterations during training
    # plot_dcec_tsne(
    #     model=model,
    #     models_directory=os.path.join(cfg.models, cfg.exp, 'dcec'),
    #     figures=os.path.join(cfg.figures, cfg.exp, 'dcec'),
    #     dataset=x_test
    # )

    # # plot train metrics
    # plot_train_metrics(
    #     file=os.path.join(cfg.tables, cfg.exp, 'dcec_train_metrics.csv'),
    #     save_dir=os.path.join(cfg.figures, cfg.exp, 'dcec')
    # )

    # metrics, y_pred = test_dcec(model, x_test, y_test)
    # plot_confusion_matrix(
    #     y_true=y_test,
    #     y_pred=y_pred,
    #     save_dir=os.path.join(cfg.figures, cfg.exp, 'dcec')
    # )
    # print('final metrics:', metrics)

# TODO https://machinelearningmastery.com/how-to-visualize-filters-and-feature-maps-in-convolutional-neural-networks/