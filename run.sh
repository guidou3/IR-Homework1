# author: Guido Santi
# date  : 10/01/2019

## SETUP
echo "+++ SETUP +++"
if [ -d "terrier-core-4.4" ]; then2
    mv terrier-core-4.4 terrier
fi

if [ ! -d terrier ]; then
    echo "--- terrier directory not found! ---"
    exit 1
fi

python rename.py

os.system("uncompress data/TIPSTER/**/**/* -q")
os.system("uncompress data/TIPSTER/TREC_VOL4/**/**/*")

mv terrier/etc/terrier.properties terrier/etc/terrier.properties.bak
cp terrier.properties terrier/etc/terrier.properties

sh terrier/bin/trec_setup.sh data/TIPSTER/

if [ ! -d "terrier/var" ]
then
    mkdir terrier/var
fi

if [ ! -d "terrier/var/indexes" ]
then
    mkdir terrier/var/indexes
fi

if [ -d "terrier/var/indexes/both" ]
then
    rm -r terrier/var/indexes/both
fi
mkdir terrier/var/indexes/both

if [ -d "terrier/var/indexes/stemmer" ]
then
    rm -r terrier/var/indexes/stemmer
fi
mkdir terrier/var/indexes/stemmer

if [ -d "terrier/var/indexes/nothing" ]
then
    rm -r terrier/var/indexes/nothing
fi
mkdir terrier/var/indexes/nothing

## INDEXING
echo "+++ INDEXING +++"

index_both() {
    sh terrier/bin/trec_terrier.sh -i -Dterrier.index.path=indexes/both -Dtermpipelines=Stopwords,PorterStemmer  
}

index_stemmer() {
    sh terrier/bin/trec_terrier.sh -i -Dterrier.index.path=indexes/stemmer -Dtermpipelines=PorterStemmer
}

index_nothing() {
    sh terrier/bin/trec_terrier.sh -i -Dterrier.index.path=indexes/nothing -Dtermpipelines=
}

# run indexing concurrently
index_both & index_stemmer & index_nothing

# wait for indexing to end
wait

# reset the current properties to my default values
cp terrier.properties terrier/etc/terrier.properties


# RETRIVAL
echo "+++ RETRIVAL +++"

sh terrier/bin/trec_terrier.sh -r -Dterrier.index.path=indexes/both -Dtrec.results.file=bm25_both.res \
-Dtrec.model=BM25 -Dtermpipelines=Stopwords,PorterStemmer

sh terrier/bin/trec_terrier.sh -r -Dterrier.index.path=indexes/both -Dtrec.results.file=tf_idf_both.res \
-Dtrec.model=TF_IDF -Dtermpipelines=Stopwords,PorterStemmer

sh terrier/bin/trec_terrier.sh -r -Dterrier.index.path=indexes/stemmer -Dtrec.results.file=bm25_stemmer.res \
-Dtrec.model=BM25 -Dtermpipelines=PorterStemmer

sh terrier/bin/trec_terrier.sh -r -Dterrier.index.path=indexes/nothing -Dtrec.results.file=tf_idf_nothing.res \
-Dtrec.model=TF_IDF -Dtermpipelines=


# EVALUATION
echo "+++ EVALUATION +++"
if [ -d evaluated ]
then
	rm -r evaluated
fi
mkdir evaluated

sh terrier/bin/trec_eval.sh -q -m all_trec data/qrels.trec7.txt terrier/var/results/bm25_both.res > evaluated/bm25_both.txt

sh terrier/bin/trec_eval.sh -q -m all_trec data/qrels.trec7.txt terrier/var/results/tf_idf_both.res > evaluated/tf_idf_both.txt

sh terrier/bin/trec_eval.sh -q -m all_trec data/qrels.trec7.txt terrier/var/results/bm25_stemmer.res > evaluated/bm25_stemmer.txt

sh terrier/bin/trec_eval.sh -q -m all_trec data/qrels.trec7.txt terrier/var/results/tf_idf_nothing.res > evaluated/tf_idf_nothing.txt


# ANOVA & PLOTS
python -W ignore test.py
