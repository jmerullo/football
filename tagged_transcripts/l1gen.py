"""
"L1 SAGE": a BOW text model that assumes words are generated as log-linear
sparse additive combinations of their documents' metadata features.

x = word counts in a doc
y = doc's (non-textual, metadata) feature a.k.a. covariate vector
Both x and y are observed.
p(x | y) = (1/Z) exp(beta + y*gamma)
p(x_w | y) = (1/Z) exp(beta_w + y'gamma_{.,w})
where every gamma_{k,w} ~ Laplace(1/lambda)

beta (V): background log-probs (set to empirical corpus MLE)
gamma (KxV): per-feature weights across word vocabulary

If y is one-hot, it's a single-membership multiclass model, similar to
Multinomial NB except with a shared background component.  If y is not one-hot,
it's more interesting: for example, multiple covariate-lexical effects can be
present at once.

Similar to Eisenstein's "SAGE" model, except uses L1 regularization or MAP
estimation, instead of VB under a different hierarchical model.  See also
Taddy's "inverse regression" model.  This implmentation uses OWL-QN, via
PyLibLBFGS, for the convex optimization training.
"""
# initialized from katie's codebase: https://github.com/slanglab/docprop/blob/master/code/loglin/model.py
from __future__ import division, print_function
import time, json, glob, sys
import numpy as np

from scipy.special import logsumexp
# https://github.com/cvxgrp/cvxpy/issues/640
#from scipy.misc import logsumexp
from lbfgs import LBFGS, LBFGSError, fmin_lbfgs

#for the pylbfgs package 
def nll_and_grad(gamma, grad, beta, trainX, trainY):
    '''
    gamma:: the "corruption" vectors (class-specific vector), size KxV
    grad:: gradient of gamma, also KxV. This will be zerod and mutated.
    beta:: background logprobs (weights)
    '''
    assert grad.shape == gamma.shape
    K, V = gamma.shape
    D = trainY.shape[0]
    assert D != V, "stupid limitation sorry"
    assert beta.shape == (V,)
    assert np.all(np.isfinite(beta)), "bad beta"
    assert np.all(np.isfinite(gamma)), "bad gamma"

    # pyliblbfgs wants 'grad' updated in-place.
    # need to zero it out before incrementally adding in-place.
    grad.fill(0.0) 

    # precompute unnormalized LMs for every doc as one big dense matrix
    # we could do minibatches instead to save memory.
    doc_lprobs = trainY.dot( gamma )
    assert doc_lprobs.shape == (D,V)
    doc_lprobs += beta  ## should broadcast to every row.

    # could use logsumexp(axis) to batch this?
    ll = 0.0
    for i in range(D):
        w_lprobs = doc_lprobs[i] - logsumexp(doc_lprobs[i])
        w_probs = np.exp(w_lprobs)
        doclen = np.sum(trainX[i])
        assert np.all(np.isfinite(w_lprobs))

        ll += trainX[i].dot(w_lprobs)

        # dl/gamma_{j,w} = y_j (x_w - doclen*p(w | y))
        wordpred = doclen * w_probs
        residvec = trainX[i] - wordpred
        assert residvec.shape == (V,)
        grad += np.outer(trainY[i], residvec)
        # same as:
        # for k in xrange(K): grad[k] += trainY[i,k] * residvec

    #switch to negative for minimization. note this is INPLACE mutation
    grad *= -1.0
    return -ll

def progress(weights, grad, fx, xnorm, gnorm, step, k, num_eval, *args):
    """https://github.com/larsmans/pylbfgs/blob/master/lbfgs/_lowlevel.pyx#L291"""
    print("iter {k} linestep {step} nnz {nnz} nll {fx} weight,grad norms {xnorm} {gnorm}".format(nnz=np.sum(weights!=0), **locals()))
    # return non-zero to stop the optimizer? or is this buggy?
    # if k>5: return -1
    return 0

#########################

def train(trainX, trainY, l1_penalty=1e-5, epsilon=1e-3, delta=1e-3, verbose=True):
    """
    Inputs:
        trainX (D,V): for each doc, vector of word counts
        trainY (D,K): for each doc, vector of doc covariates, e.g. binary vector
    where
        D = number of docs
        V = number of wordtypes in vocabulary
        K = number of doc features

    Returns:
        The 'gamma' (K x V) weights matrix of sparse differences of words'
        log-probabilities relative to the background distribution.  See
        module's docs for details on the model.

    Model hyperparams:
        l1_penalty: the 'lambda' in the penalty term lambda*||gamma||_1.
        Make this higher, like 1 or 10, for more sparsity.

    Training hyperparams:
        epsilon: convergence threshold, relative grad norm
        delta: convergence threshold, relative change in objective

    """
    D1,V = trainX.shape
    D2,K = trainY.shape
    assert D1==D2, "matrices should both have 1 row per doc"
    D=D1
    if verbose:
        print("{} docs, {} vocab, {} doc features".format(D,V,K))

    bb=LBFGS()
    bb.orthantwise_c = l1_penalty
    bb.linesearch = 'wolfe'
    # looks like it's an OR between the two convergence criteria.
    # https://github.com/larsmans/pylbfgs/blob/master/liblbfgs/lbfgs.c#L498
    bb.epsilon = epsilon
    bb.delta = delta

    corpus_wordcounts = trainX.sum(0)
    assert np.all(corpus_wordcounts > 0), "can't handle zero counts in input"
    corpus_wordprob = corpus_wordcounts / corpus_wordcounts.sum()
    beta = np.log(corpus_wordprob)

    weight_init = np.zeros((K,V))
    cb = progress if verbose else lambda *a: 0
    gamma = bb.minimize(nll_and_grad, weight_init, cb, [beta, trainX, trainY])
    return gamma, beta

