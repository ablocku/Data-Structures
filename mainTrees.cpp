#include <iostream>
#include <fstream>
using namespace std;

ifstream f("date.in");
ofstream g("date.out");

struct nod
{
    int inf;
    nod *tata, *st, *dr;
    nod(const int val = 0, nod *t = nullptr, nod *s = nullptr, nod *d = nullptr): inf(val), tata(t), st(s), dr(d){}
};

typedef nod* pnod;

pnod r;

//rotim de la nodul x la stanga lui
void leftRotate(pnod x)
{
    pnod y = x->dr;
    if(x->dr)
        x->dr = y->st;
    if(y->st)
        y->st->tata = x;

    y->tata = x->tata;
    if(x->tata == nullptr)
    {
        if(x == r)
            r = y;
    }
    else
        if(x == x->tata->st)
            x->tata->st = y;
        else
            x->tata->dr = y;
    y->st = x;
    x->tata = y;
}

//rotim de la nodul x la dreapta lui
void rightRotate(pnod x)
{
    pnod y = x->st;
    if(x->st)
        x->st = y->dr;
    if(y->dr)
        y->dr->tata = x;
    y->tata = x->tata;
    if(x->tata == nullptr)
    {
        if(x == r)
            r = y;
    }
    else
        if(x == x->tata->st)
            x->tata->st = y;
        else
            x->tata->dr = y;
    y->dr = x;
    x->tata = y;
}


void splay(pnod x)
{
    if(!x)
        return ;
    while(x->tata)
    {
        if(x->tata->tata == nullptr) //zig
        {
            if(x->tata->st == x)
                rightRotate(x->tata);
            else
                leftRotate(x->tata);
        }
        else
        {
            if(x->tata->st == x)
            {
                if(x->tata->tata->st == x->tata) //zig-zig
                {
                    rightRotate(x ->tata->tata);
                    rightRotate(x->tata);
                }
                else //zig-zag
                {
                    rightRotate(x->tata);
                    leftRotate(x->tata);
                }
            }
            else
                if(x->tata->tata->dr == x->tata)
                {
                    leftRotate(x->tata->tata);
                    leftRotate(x->tata);
                }
                else
                {
                    leftRotate(x->tata);
                    rightRotate(x->tata);
                }
        }

    }
}

pnod rightMax(pnod x)
{
    if(!x)
        return nullptr;
    pnod x_ = x -> dr;
    while(x_)
        x_ = x_ -> dr;
    return x_;
}

pnod leftMin(pnod x)
{
    if(!x)
        return nullptr;
    pnod x_ = x;
    while(x_ -> st)
        x_ = x_ -> st;
    return x_;
}

void swish(pnod x, pnod y)
{
    if(!x -> tata)
        r = y;
    else
        if(x == x -> tata -> st)
            x -> tata -> st = y;
        else
            x -> tata -> dr = y;
    if(y)
        y -> tata = x -> tata;
}

pnod predecesor(int x) //returneaza un pointer catre predecesorul intului primit
{
    pnod nodCrt = r, pred = nullptr; //nodCrt - nodul curent, pred - predecesorul
    while(nodCrt)
    {
        if(x == nodCrt -> inf) //l-am gasit
        {
            splay(nodCrt);
            return nodCrt;
        }
        if(x < nodCrt -> inf)
            nodCrt = nodCrt -> st;
        else
            {
            pred = nodCrt;
            nodCrt = nodCrt -> dr;
            }
    }
    splay(pred);
    return pred;
}

pnod succesor(int x) //returneaza un pointer catre succesorul intului primit
{
    pnod nodCrt = r, pred = nullptr;
    while(nodCrt)
    {
        if(x == nodCrt -> inf) //l-am gasit
        {
            splay(nodCrt);
            return nodCrt;
        }
        if(x > nodCrt -> inf)
            nodCrt = nodCrt -> dr;
        else
        {
            pred = nodCrt;
            nodCrt = nodCrt -> st;
        }
    }
    splay(pred);
    return pred;
}

pnod search(int x) //returneaza un pointer catre nodul in care se afla intul primit
{
    pnod nodCrt = r;
    while(nodCrt)
    {
        if(x == nodCrt -> inf) //l-am gasit
        {
            splay(nodCrt);
            return nodCrt;
        }
        if(x < nodCrt -> inf)
            nodCrt = nodCrt -> st;
        else
            nodCrt = nodCrt -> dr;
    }
    return nullptr;
}

void add(int x) //adauga un element nou la splayTree, daca nu e deja in el
{
    pnod nodCrt = r, pred = nullptr;
    while(nodCrt)
    {
        pred = nodCrt;
        if(x == nodCrt -> inf) //daca este deja in splayTree, nu il mai adaugam
            return ;
        if(x < nodCrt -> inf)
            nodCrt = nodCrt -> st;
        else
            nodCrt = nodCrt -> dr;
    }
    nodCrt = new nod(x,pred);
    if(!pred)
        r = nodCrt;
    else
        if(x < pred -> inf)
            pred -> st = nodCrt;
        else
            pred -> dr = nodCrt;
    splay(nodCrt);
}

void del(int x)
{
    pnod nodCrt = search(x);
    if(!nodCrt)
        return ;
    splay(nodCrt);
    if(!nodCrt->st)
        swish(nodCrt, nodCrt->dr);
    else
        if(!nodCrt->dr)
            swish(nodCrt, nodCrt -> st);
        else
        {
            pnod mini = leftMin(nodCrt -> dr);
            if(mini->tata != nodCrt)
            {
                swish(mini, mini -> dr);
                mini -> dr = nodCrt -> dr;
                mini -> dr -> tata = mini;
            }
            swish(nodCrt, mini);
            mini -> st = nodCrt -> st;
            mini -> st -> tata = mini;
        }
}

void afisareSortat(int a, int b)
{
    int x = a;
    bool ok = true;
    while(ok)
    {
        pnod check = succesor(x);
        if(!check or check->inf > b)
            break;
        g << check->inf << ' ';
        x = check->inf + 1;
    }
    g << '\n';
}

void runTests()
{
    int T, p, x;
    f >> T;
    while(T--)
    {
        f >> p >> x;
        //g << p << x <<'\n';
        if(p == 1)
        {
            pnod p = search(x);
            if(p == nullptr)
                g << "Elementul " << x << " nu a fost gasit" << '\n'<< '\n';
            else
                g << "Elementul " << x << " apartine arborelui" << '\n'<< '\n';
        }
        if(p == 2)
        {
            g << "Adaugam la arbore elementul " << x << '\n'<< '\n';
            add(x);
        }
        if(p == 3)
        {
            g << "Stergem din arbore elementul " << x << '\n'<< '\n';
            del(x);
        }
        if(p == 4)
            g << "Succesorul lui " << x << " este " << succesor(x) -> inf << '\n'<< '\n';
        if(p == 5)
            g << "Predecesorul lui " << x << " este " << predecesor(x) -> inf << '\n'<< '\n';
        if(p == 6)
        {
            int y;
            f >> y;
            afisareSortat(x,y);
            g << '\n';
        }
    }
}

int main()
{
    runTests();
    return 0;
}
