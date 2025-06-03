# Progetto d'Esame Enrico Cornacchia - Programmazione di Applicazioni Data Intensive

Questo repository contiene il progetto d'esame svolto per il corso di **Programmazione di Applicazioni Data Intensive** (DISI - Università di Bologna, Cesena).

## Contenuto

- File Jupyter Notebook (`.ipynb`) con codice, analisi, commenti e risultati.
- I dati utilizzati e le fonti sono indicati all'interno del notebook.
- Una web app Flask per la predizione del successo di campagne Kickstarter.

---

## Come eseguire la web app

1. **Installare le dipendenze**

   Spostarsi nella cartella `PROGETTO_ESAME/Data_Intensive_Project/webapp` ed eseguire:

   ```sh
   pip install -r requirements.txt
   ```

2. **Assicurarsi che il file del modello `mlp_kickstarter.pkl` sia presente nella stessa cartella della web app**  
   (o nel percorso corretto specificato in `app.py`).

3. **Avviare il server Flask**

   Sempre dalla cartella `webapp`, eseguire:

   ```sh
   python app.py
   ```

   Dopo pochi secondi si aprirà automaticamente il browser sulla pagina della web app.

4. **Utilizzo**

   Compilare il form con le caratteristiche del progetto Kickstarter e premere "Predict" per ottenere la previsione di successo.

---