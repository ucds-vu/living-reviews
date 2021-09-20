#!/bin/sh
OUTPUT="./data/toLoad/"


python3 ./main.py
~/Documents/np mktrusty -r ../np/dois.trig ../np/relations.trig ../np/studies.trig ../np/papers.trig ../np/reviews.trig
~/Documents/np op filter --out-format nq ../np/trusty.papers.trig > ${OUTPUT}paper_nanopubs.nq
~/Documents/np op filter --out-format nq ../np/trusty.studies.trig > ${OUTPUT}studies_nanopubs.nq
~/Documents/np op filter --out-format nq ../np/trusty.relations.trig > ${OUTPUT}relations_nanopubs.nq
~/Documents/np op filter --out-format nq ../np/trusty.dois.trig > ${OUTPUT}dois_nanopubs.nq
~/Documents/np op filter --out-format nq ../np/trusty.reviews.trig > ${OUTPUT}reviews_nanopubs.nq
~/Documents/np op filter --out-format nq ../np/trusty.vocab.trig > ${OUTPUT}vocab_nanopubs.nq
