#include <iostream>
#include <fstream>
#include <bits/stdc++.h>
#include <ctime>

using namespace std;


ifstream f("date.in");
ofstream g("date.out");

bool sorted(int v[], int n)
{
    for(int i = 0; i < n; ++i)
        if(v[i] > v[i+1])
            return false;
    return true;
}


void bubbleSort(int v[], int n)
{
    bool ok;
    do
    {
        ok = true;
        for(int i = 0; i < n-1 ; ++i)
            if(v[i] > v[i+1])
                {
                int aux = v[i];
                v[i] = v[i+1];
                v[i+1] = aux;
                ok = false;
                }
        n--;
    }
    while(!ok);
}

void countSort(int v[], int n)
{
    int *cnt;
    int maxi = v[0], mini = v[0];
    for(int i = 1; i < n; ++i)
        {
        if(maxi < v[i])
            maxi = v[i];
        if(mini > v[i])
            mini = v[i];
        }
    if(mini > 0)
        {
        cnt = new int[maxi+1];
        for(int i = 0; i <= maxi; ++i)
            cnt[i] = 0;
        for(int i = 0; i < n; ++i)
            cnt[v[i]] += 1;
        int poz = 0;
        for(int i = 0; i <= maxi; ++i)
            for(int j = 1; j <= cnt[i]; ++j)
                v[poz++] = i;
        }
    else
        {
        int m = maxi+(mini*-1)+1;
        cnt = new int[m];
        for(int i = 0; i <= m; ++i)
            cnt[i] = 0;
        for(int i = 0; i < n; ++i)
            cnt[v[i]-mini] += 1;
        int poz = 0;
        for(int i = 0; i <= m; ++i)
            for(int j = 1; j <= cnt[i]; ++j)
                v[poz++] = i + mini;
        }
}

int partitionare(int v[], int p, int q)
{
    int x = v[p];
    int i, j;
    i = p + 1;
    j = q;
    while(i <= j)
        {
        if(v[i] <= x)
            ++i;
        if(v[j] >= x)
            --j;
        if(v[i] > x and v[j] < x and i < j)
            {
            int aux = v[i];
            v[i] = v[j];
            v[j] = aux;
            ++i;
            --j;
            }
        }
    v[p] = v[j];
    v[j] = x;
    return j;
}

void quickSort(int v[], int p, int q)
{
    int k = partitionare(v, p, q);
    if(p < k-1)
        quickSort(v, p, k-1);
    if(k+1 < q)
        quickSort(v, k+1, q);
}

void interclasare(int v[], int p, int q, int mij)
{
    int *rez;
    rez = new int[p + q];
    int i, j, k;
    k = 0;
    i = p;
    j = mij + 1;
    while(i <= mij and j <= q)
        {
        if(v[i] < v[j])
            rez[k++] = v[i++];
        else
            rez[k++] = v[j++];
        }
    while(i <= mij)
        rez[k++] = v[i++];
    while(j <= q)
        rez[k++] = v[j++];
    for(i = 0, j = p; i < k; i++, j++)
        v[j] = rez[i];
}

void mergeSort(int v[], int p, int q)
{
    if(p < q)
        {
        int mij = (p + q) / 2;
        mergeSort(v, p, mij);
        mergeSort(v, mij+1, q);
        interclasare(v, p, q, mij);
        }
}

void cntRad(int v[], int n, int exp)
{
    int rez[n];
    int i, count[10];
    for(i = 0; i < 10; ++i)
        count[i] = 0;
    for(i = 0; i < n; ++i)
        count[(v[i] / exp) % 10]++;
    for(i = 1; i < 10; ++i)
        count[i] += count[i-1];
    for(i = n-1; i >= 0; i--)
        {
        rez[count[(v[i] / exp) % 10] - 1] = v[i];
        count[(v[i] /exp) % 10]--;
        }
    for(i = 0; i < n; ++i)
        v[i] = rez[i];
}

void radixSort(int v[], int n)
{
    int maxi = abs(v[0]);
    int i, exp;
    for(i = 1; i < n; ++i)
        if(abs(v[i]) > maxi)
            maxi = v[i];
    for(exp = 1; maxi/exp > 0; exp *= 10)
        cntRad(v, n, exp);
}

void afisare(int v[], int n)
{
    for(int i = 0; i < n; ++i)
        g<<v[i]<<' ';
    g<<'\n';
}

int * genSir(int n, int maxi)
{
    int *v;
    v = new int[n];
    for(int i = 0; i < n; ++i)
        v[i] = rand()%maxi+ 1;
    return v;
}

void reset(int v[], int s[], int n)
{
    for(int i = 0; i < n; ++i)
        s[i] = v[i];
}

int maxim(int v[], int n)
{
    int maxi = v[0];
    for(int i = 1; i < n; ++i)
        if(v[i] > maxi)
            maxi = v[i];
    return maxi;
}

void runSorts(int v[], int n)
{
    int *s;
    s = new int[n];
    reset(v,s,n);
    clock_t start, stop;
    if(n > 10000)
        g<<"--> Nu putem face BubbleSort"<<'\n';
    else
        {
        start = clock();
        bubbleSort(s,n);
        stop = clock();
        if(sorted(s,n))
            g<<"Algoritmul este corect --> BubbleSort a durat: "<<double(stop - start) / CLOCKS_PER_SEC<<'\n';
        else
            g<<"Elementele nu s-au sortat corect"<<'\n';
        reset(v,s,n);
        }
    if(maxim(v,n) > 1000000)
        g<<"--> Nu putem face CountSort"<<'\n';
    else
        {
        start = clock();
        countSort(s,n);
        stop = clock();
        if(sorted(s,n))
            g<<"Algoritmul este corect --> CountSort a durat: "<<double(stop - start) / CLOCKS_PER_SEC<<'\n';
        else
            g<<"Elementele nu s-au sortat corect"<<'\n';
        reset(v,s,n);
        }
    start = clock();
    quickSort(s,0,n-1);
    stop = clock();
    if(sorted(s,n))
        g<<"Algoritmul este corect --> QuickSort a durat: "<<double(stop - start) / CLOCKS_PER_SEC<<'\n';
    else
        g<<"Elementele nu s-au sortat corect"<<'\n';
    reset(v,s,n);
    start = clock();
    mergeSort(s,0,n-1);
    stop = clock();
    if(sorted(s,n))
        g<<"Algoritmul este corect --> MergeSort a durat: "<<double(stop - start) / CLOCKS_PER_SEC<<'\n';
    else
        g<<"Elementele nu s-au sortat corect"<<'\n';
    reset(v,s,n);
    start = clock();
    radixSort(s,n);
    stop = clock();
    if(sorted(s,n))
        g<<"Algoritmul este corect --> RadixSort a durat: "<<double(stop - start) / CLOCKS_PER_SEC<<'\n';
    else
        g<<"Elementele nu s-au sortat corect"<<'\n';
    g<<'\n'<<'\n';
}


int main()
{
int n, maxi;
int *v;
int teste;
f>>teste;
for(int i = 1; i <= teste; ++i)
    {
    f>>n>>maxi;
    v = genSir(n, maxi);
    afisare(v,n);
    runSorts(v, n);
    }
return 0;
}
