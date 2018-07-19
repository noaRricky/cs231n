import numpy as np
from random import shuffle


def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops).

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    # compute the loss and the gradient
    num_classes = W.shape[1]
    num_train = X.shape[0]
    loss = 0.0
    # initialize gradients
    dW = np.zeros(W.shape)
    for i in range(num_train):
        scores = X[i].dot(W)
        correct_class_score = scores[y[i]]
        loss_contributors_count = 0
        for j in range(num_classes):
            if j == y[i]:
                continue
            margin = scores[j] - correct_class_score + 1  # note delta = 1
            if margin > 0:
                loss += margin
                # incorrect class gradients
                dW[:, j] += X[i]
                # count contributor terms to loss
                loss_contributors_count += 1
        # correct class gradient
        dW[:, y[i]] += (-1) * loss_contributors_count * X[i]

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train
    dW /= num_train

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W * W)

    # Compute the gredients for regulariztion loss
    dW += reg * W

    #############################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    #############################################################################

    return loss, dW


def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero
    num_train = X.shape[0]

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the structured SVM loss, storing the    #
    # result in loss.                                                           #
    #############################################################################
    scores = np.dot(X, W)
    # print('scores shape: {}'.format(scores.shape))
    lines = np.arange(num_train)
    correct_class_scores = scores[lines, y][:, np.newaxis]
    # print('correct_class_scores shape: {}'.format(correct_class_scores.shape))
    margin = scores - correct_class_scores + 1
    margin_activate_idxs = margin > 0
    loss += np.sum(margin[margin_activate_idxs]) + 0.5 * reg * np.sum(W * W)

    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the gradient for the structured SVM     #
    # loss, storing the result in dW.                                           #
    #                                                                           #
    # Hint: Instead of computing the gradient from scratch, it may be easier    #
    # to reuse some of the intermediate values that you used to compute the     #
    # loss.                                                                     #
    #############################################################################
    X_mask = np.zeros(margin.shape)
    X_mask[margin_activate_idxs] = 1
    X_mask[lines, y] -= np.sum(X_mask, axis=1)
    dW += np.dot(X.T, X_mask)
    dW /= num_train
    dW += reg * W
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################

    return loss, dW


if __name__ == '__main__':
    train_dev = np.array([[1, 2, 3], [2, 2, 2], [2, 4, 1]])  # shape 3 * 3
    W_dev = np.random.randn(2, 3)
    y = np.array([1, 0, 1])
    reg = 0.1
    svm_loss_vectorized(train_dev, W_dev, y, reg)
