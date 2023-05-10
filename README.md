# Semantic search on logs

## Setup environment

```bash
conda create --name=qdrant1       
conda activate qdrant1                  
```

## Install dependencies

```bash
pip3 install -r requirements.txt
```

## Add data


```bash
python3 logs_add.py
```

## search data

```bash
python3 logs_search.py
```
