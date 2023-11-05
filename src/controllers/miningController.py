from flask import render_template, request, redirect, url_for, flash
import time
from app import db
from src.models.transaction import Transaction
from src.mining_algorithms.eclat import Eclat
from src.mining_algorithms.association_rule import associationRule
from src.models.mining import MiningProcess, AssociationResult, AssociationResultProduct
import datetime


def eclatIndex():
    return render_template("mining/eclat.html")


def eclatStoreMining(period_start, period_end, minimum_support, minimum_confidence, rules, lenOfTransaction, execution_time):
    # Mining Process
    mining_process = MiningProcess(
        algorithm='ECLAT',
        period_start=period_start,
        period_end=period_end,
        minimum_support=minimum_support,
        minimum_confidence=minimum_confidence,
        execution_time=execution_time,
         created_at=datetime.datetime.now()
    )
    
    db.session.add(mining_process)
    db.session.commit()
    
    # Association Results
    # for item in rules:
        # antecedent = item[0]
        # consequent = item[1]
        # support = item[2]
        # confidence = item[3]
        # lift = item[4]
    for item in rules.items():
        print("item", item)
        antecedent = item[0][0]
        consequent = item[0][1]
        support = item[1][0]
        confidence = item[1][1]
        lift = item[1][2]

        # Membuat entri di tabel association_results
        association_result = AssociationResult(
            mining_process_id=mining_process.id,
            support=support / lenOfTransaction,
            confidence=confidence,
            lift=lift
        )
        db.session.add(association_result)
        db.session.flush()

        # Memasukkan antecedent ke tabel association_product_results
        for itemCode in antecedent:
            association_result_product_antecedent = AssociationResultProduct(
                association_result_id=association_result.id,
                itemCode=itemCode,
                is_antecedent=True
            )
            db.session.add(association_result_product_antecedent)

        # Memasukkan consequent ke tabel association_product_results
        for itemCode in consequent:
            association_result_product_consequent = AssociationResultProduct(
                association_result_id=association_result.id,
                itemCode=itemCode,
                is_antecedent=False
            )
            db.session.add(association_result_product_consequent)

    db.session.commit()


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

    eclatStoreMining(startDate, endDate, supportRatio, ConfidenceRatio, rules, lenOfTransaction, execution_time)
    
    return render_template("mining/eclat.html",
                           parameters=parameters,
                           parameters_label_mapping=parameters_label_mapping,
                           verticalData=verticalData, 
                           lenOfTransaction=lenOfTransaction, 
                           rules=rules,
                           freqItems=freqItems,
                           execution_time=execution_time)
    

def fpGrowthIndex():
    return render_template("mining/fp-growth.html")


def fpGrowthMining():
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
    
    # Algorithm here
    
    
    time.sleep(2) 
    end_time = time.time()
    execution_time = end_time - start_time
    
    return render_template("mining/fp-growth.html",
                           execution_time=execution_time)