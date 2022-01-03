#include "BST.h"

NodoBST::NodoBST(Studenti* stud){
    this->stud = stud;
    this->dx = NULL;
    this->sx = NULL;
    this->parent = NULL;
}

Studenti* NodoBST::getStud(){
    return stud;
}

void NodoBST::setSx(NodoBST* newSx){
    sx = newSx;
}

void NodoBST::setDx(NodoBST* newDx){
    dx = newDx;
}

void NodoBST::setParent(NodoBST* newParent){
    parent = newParent;
}

NodoBST* NodoBST::getSx(){
    return sx;
}

NodoBST* NodoBST::getDx(){
    return dx;
}

NodoBST* NodoBST::getParent(){
    return parent;
}

NodoBST* BST::getRoot(){
    return root;
}

BST::BST(){
    root = NULL;
}

void BST::inserisci(Studenti* newStud){
    NodoBST* newNodo = new NodoBST(newStud);
    NodoBST* app = root;
    NodoBST* parentApp;

    if(root == NULL)
        root = newNodo;
    else{
        while(app != NULL){
            parentApp = app;
            
            if(newStud->getMedia() < app->getStud()->getMedia())
                app = app->getSx();
            else
                app = app->getDx();
        }         

        newNodo->setParent(parentApp);

        if(newStud->getMedia() < parentApp->getStud()->getMedia())
            parentApp->setSx(newNodo);
        else
            parentApp->setDx(newNodo);  
    }
}

void BST::inOrder(NodoBST* nodoAttuale){
    if(nodoAttuale->getSx() != NULL)
        inOrder(nodoAttuale->getSx());
    
    Studenti* studente = nodoAttuale->getStud();
    cout << "Cognome: " << studente->getCognome() << 
                " | nome: " << studente->getNome() << 
                " | matricola: " << studente->getMatricola() <<
                " | anno Immatricolazione: " << studente->getAnno() <<
                " | media: " << studente->getMedia() << endl;

    if(nodoAttuale->getDx() != NULL)
        inOrder(nodoAttuale->getDx());
}

int BST::getNStudenti(NodoBST* nodoAttuale){
    int sommaDestra = 0;
    int sommaSinistra = 0;

    if(nodoAttuale->getDx() != NULL)
        sommaDestra = getNStudenti(nodoAttuale->getDx());

    if(nodoAttuale->getSx() != NULL)
        sommaSinistra = getNStudenti(nodoAttuale->getSx());

    return 1 + sommaSinistra + sommaDestra;
}

double BST::getMedia(NodoBST* nodoAttuale, bool primo){
    double sommaDestra = 0;
    double sommaSinistra = 0;
    double sommaTotale = 0;
    
    if(nodoAttuale->getDx() != NULL)
        sommaDestra = getMedia(nodoAttuale->getDx(), false);

    if(nodoAttuale->getSx() != NULL)
        sommaSinistra = getMedia(nodoAttuale->getSx(), false);

    sommaTotale = nodoAttuale->getStud()->getMedia() + sommaDestra + sommaSinistra;

    if(primo)
        return sommaTotale / getNStudenti(nodoAttuale);
    else
        return sommaTotale;    
}

NodoBST* BST::getMin(NodoBST* nodoPartenza){
    NodoBST* app = nodoPartenza;

    while(app != NULL && app->getSx() != NULL){
        app = app->getSx();
    }

    return app;
}

NodoBST* BST::getMax(NodoBST* nodoPartenza){
    NodoBST* app = nodoPartenza;

    while(app != NULL && app->getDx() != NULL){
        app = app->getDx();
    }

    return app;
}

void BST::elimina(int nStudenti){
    NodoBST* app;
    
    for(int i = 0; i < nStudenti; i++){
        app = getMin(root);

        if(app == NULL)
            return;
        else if(app->getParent() == NULL)
            root = app->getDx();
        else{
            app->getParent()->setSx(app->getDx());
            
            if(app->getDx() != NULL)
                app->getDx()->setParent(app->getParent());
        }
    }

    for(int i = 0; i < nStudenti; i++){
        app = getMax(root);

        if(app == NULL)
            return;
        else if(app->getParent() == NULL)
            root = app->getSx();
        else{
            app->getParent()->setDx(app->getSx());
            
            if(app->getSx() != NULL)
                app->getSx()->setParent(app->getParent());
        }
    }
}