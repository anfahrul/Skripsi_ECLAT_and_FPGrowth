from flask import render_template, request, redirect, url_for, flash
import time
from app import db
from src.models.transaction import Transaction
from src.mining_algorithms.eclat import Eclat
from src.mining_algorithms.association_rule import associationRule


def eclatIndex():
    return render_template("mining/eclat.html")


def eclatMining():
    start_time = time.time()

    request_form = request.form.to_dict()
    
    startDate = request_form['start-date']
    endDate = request_form['end-date']
    supportRatio = float(request_form['support'])
    ConfidenceRatio = float(request_form['confidence'])
    
    parameters = {
        'startDate': startDate,
        'endDate': endDate,
        'supportRatio': supportRatio,
        'ConfidenceRatio': ConfidenceRatio
        }
    
    parameters_label_mapping = {
        'startDate': 'Tanggal Mulai',
        'endDate': 'Tanggal Akhir',
        'supportRatio': 'Minimum Support',
        'ConfidenceRatio': 'Minimum Confidence'
    }

    
    transactions = Transaction.query.all()
    lenOfTransaction = len(transactions)
    
    # minimumSupport = supportRatio * len(transactions)
    minsup = 2
    eclatInstance = Eclat(minsup=minsup)
    listOfItemInTransaction, verticalData, freqItems = eclatInstance.run()
    
    rules = associationRule(freqItems, listOfItemInTransaction, 0.75)
    
    time.sleep(2) 
    end_time = time.time()
    execution_time = end_time - start_time
    
    return render_template("mining/eclat.html",
                           parameters=parameters,
                           parameters_label_mapping=parameters_label_mapping,
                           verticalData=verticalData, 
                           lenOfTransaction=lenOfTransaction, 
                           rules=rules,
                           freqItems=freqItems,
                           execution_time=execution_time)