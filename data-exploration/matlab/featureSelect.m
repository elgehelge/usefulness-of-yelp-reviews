close all; clear all; clc;

%% Load data

[A, rows, cols, entries, rep, field, symm] = mmread('/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/python code/finalMatrix.mtx');

%% NMF
Winit = ;
Hinit = ;
[W,H] = nmf(A, Winit, Hinit, tol, timelimit, maxiter);

%% LASSO

B = lasso(A(:,2:cols),A(:,1));

%% Forward selection
opts = statset('display','iter');

fun = @(x0,y0,x1,y1) norm(y1-x1*(x0\y0))^2;  % residual sum of squares


X = A(:,2:cols);
y = A(:,1);

inmodel = sequentialfs(fun, X, y, 'options', opts)