#! /usr/bin/python3

"""

Script for testing a random number generator by calculating
some statistical estimators.

"""


import sys;
import random;
import math;


"""
  Function: Returns a list of floating-point random numbers uniformly
  distributed between 0 and 1.
  Usage:
    rnlist = getnums(n, a, b);

  Input:
    n      = number of floating-point numbers to generate
    a, b   = interval for the uniformly distributed floating-point numbers

  Output:
    rnlist = list of random numbers
    
"""
def getnums(n, a, b):
    rnlist = [];
    for i in range(n):
        x = a + (b-a) * random.random();
        rnlist.append(x);
    return rnlist;


"""
  Function: Returns some statistical estimators.
  Usage:
  
    Function call:
    ave, sigma, skew, kurt = statest(lst);

    Output:
    ave:   average
    sigma: standard deviation (square-root of 2nd moment, a.k.a the variance)
    skew:  skewness
    kurt:  kurtosis

    Input:
    lst: list of floating-point random numbers


    ave xave:   xave = (1/N) * sum_{i=1}^N x_i
    sigma s:    s^2  = sum_i (x_i - xave)^2 / N := mu_2, second moment
                     = sum_i (x_i^2 + xave^2 - 2*x_i*xave)/N
                     = sum_i x_i^2/N + xave^2 - 2*xave*xave
                     = sum_i x_i^2/N - xave^2
    skew sk:    sk   = mu_3/mu_2^1.5
                     = mu_3/s^3
                     = (sum_i (x_i - xave)^3 / N) * 1/s^3
                     = sum_i (x_i^3 - 3*x_i^2*xave + 3*x_i*xave^2 - xave^3)/N * 1/s^3
                     = (sum_i x_i^3/N - 3*xave*sum_i x_i^2/N + 3*xave^2*xave - xave^3 )*1/s^3
                     = (sum_i x_i^3/N - 3*xave*sum_i x_i^2/N + 2*xave^3)*1/s^3
    kurt k:     k    = mu_4/mu_2^2
                     = mu_4/s^4
                     = (sum_i (x_i - xave)^4 / N) * 1/s^4
                     = sum_i (x_i^4 - 4*x_i^3*xave + 6*x_i^2*xave^2 - 4*x_i*xave^3 + xave^4)/N *1/s^4
                     = sum_i (x_i^4 - 4*x_i^3*xave + 6*x_i^2*xave^2 - 4*x_i*xave^3 + xave^4)/N *1/s^4
                     = (sum_i x_i^4/N - 4*xave*sum_i x_i^3/N + 6*xave^2*sum_i x_i^2/N
                     - 4*xave^3*xave + xave^4) * 1/s^4
                     = (sum_i x_i^4/N - 4*xave*sum_i x_i^3/N + 6*xave^2*sum_i x_i^2/N - 3*xave^4)*1/s^4

"""
def statest(lst):
    n = len(lst);
    sumi =0.0;
    sumi2=0.0;
    sumi3=0.0;
    sumi4=0.0;
    for i in range(n):
        sumi  += lst[i];
        sumi2 += lst[i]*lst[i];
        sumi3 += lst[i]*lst[i]*lst[i];
        sumi4 += lst[i]*lst[i]*lst[i]*lst[i];

    Ninv = 1.0/(1.0*n);
    ave = sumi * Ninv;
    sigma = math.sqrt( sumi2 *Ninv - ave*ave );
    skew = (sumi3 * Ninv - 3*ave*sumi2 * Ninv + 2*ave*ave*ave)/(sigma*sigma*sigma);
    kurt = (sumi4 * Ninv - 4*ave*sumi3 * Ninv + 6*ave*ave*sumi2 * Ninv
            - 3*ave*ave*ave*ave)/(sigma*sigma*sigma*sigma);
    return ave, sigma, skew, kurt


def main():
    n=100;
    a=0.0;
    b=1.0;
    nx = 50;
    outf = "randgentest.data";
        
    if len(sys.argv)<=1:
        print("");
        print("Usage:");
        print("    {:s} n [a [b [nx [outf]]]]".format(sys.argv[0]));
        print("Arguments:");
        print("  n       number of floating-point random numbers to generate".format(n));
        print("  a, b    interval for the uniformly distributed random numbers (a={:.6f}, b={:.6f})".format(a, b));
        print("  nx      number of data points for histogram of generated data ({:d})".format(nx));
        print("  outf    output file for histogram ({:s})".format(outf));
        print("");
        print("Default values are shown above inside the parentheses");
        print("");
        sys.exit();

    if len(sys.argv)>=2: n=int(sys.argv[1]);
    if len(sys.argv)>=3: a=float(sys.argv[2]);
    if len(sys.argv)>=4: b=float(sys.argv[3]);
    if len(sys.argv)>=5: nx=int(sys.argv[4]);
    if len(sys.argv)>=6: outf=sys.argv[5];


    lst = getnums(n, a, b);
    ave, s, sk, ku = statest(lst);
    print("Average: {:.10f}  Std.dev.: {:.10f}".format(ave, s)
        + "  Skewness: {:.10f}  Kurtosis: {:.10f}".format(sk, ku));

    """
    Create a histogram of the generated data and write to a file.
    """
    dx = (b-a)/nx;
    x = [0 for i in range(nx)];
    np = 0;
    for i in range(len(lst)):
        j = int((lst[i]-a)/dx);
        if j<0:    j=0;
        if j>=100: j=99;
        x[j]+=1;
        np+=1;

    f = open(outf, "w");
    for i in range(nx):
        f.write("{:15.10f}  {:15.10f}\n".format(i*dx, x[i]/(1.0*np)));
    f.close();
    
    

if __name__ == '__main__':
    main()

