from flask import render_template, request, redirect, url_for, flash
import time
from app import db
from src.models.transaction import Transaction
from src.models.product import Product
from src.mining_algorithms.eclat import Eclat
from src.mining_algorithms.fpgrowth import FPGrowth
from src.mining_algorithms.association_rule import associationRule, associationRuleFpGrowth
from src.models.mining import MiningProcess, AssociationResult, AssociationResultProduct
import datetime
import uuid


def eclatIndex():
    return render_template("mining/eclat.html")


def eclatStoreMining(period_start, period_end, minimum_support, minimum_confidence, rules, lenOfTransaction, execution_time):
    new_uuid = uuid.uuid4()
    process_id = str(new_uuid)
    
    # Mining Process
    mining_process = MiningProcess(
        id=process_id,
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
    for item in rules.items():
        antecedent = item[0][0]
        consequent = item[0][1]
        support = item[1][0]
        confidence = item[1][1]
        lift = item[1][2]

        # Membuat entri di tabel association_results
        association_result = AssociationResult(
            mining_process_id=mining_process.id,
            support=(support / lenOfTransaction) * 100,
            confidence=confidence * 100,
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
    
    return mining_process.id


def associateItemCodeWithName(rules):
    # Ambil data produk
    products = Product.query.all()
    product_dict = {product.itemCode: product.name for product in products}
    
    # Buat daftar aturan asosiasi dengan nama barang
    associated_rules_with_names = []

    for antecedent, consequent in rules:
        antecedent_with_names = [f"{item} - {product_dict[item]}" for item in antecedent]
        consequent_with_names = [f"{item} - {product_dict[item]}" for item in consequent]
        support, confidence, lift = rules[(antecedent, consequent)]

        associated_rules_with_names.append({
            'antecedent_with_names': antecedent_with_names,
            'consequent_with_names': consequent_with_names,
            'support': support,
            'confidence': confidence,
            'lift': lift
        })
        
    return associated_rules_with_names


def eclatMining():
    start_time = time.time()

    request_form = request.form.to_dict()
    startDate = request_form['start-date']
    endDate = request_form['end-date']
    minimumSupport = float(request_form['minimumSupport'])
    minimumConfidence = float(request_form['minimumConfidence'])
    
    parameters = {
        'startDate': startDate,
        'endDate': endDate,
        'minimumSupport': minimumSupport,
        'minimumConfidence': minimumConfidence
        }
    
    # transactions = Transaction.query.all()
    transactions_in_period = Transaction.query.filter(Transaction.date.between(startDate, endDate)).all()
    lenOfTransaction = len(transactions_in_period)
    if lenOfTransaction <=0:
        flash('Tidak ada transaksi pada periode tersebut.')
        return render_template("mining/eclat.html")
    
    minimumSupportFreq = (minimumSupport / 100) * len(transactions_in_period)
    minimumConfidenceRatio = minimumConfidence / 100
    # minsup = 2
    # minconf = 0.75
    
    eclatInstance = Eclat(minsup=minimumSupportFreq)
    listOfItemInEachTransaction, verticalData, freqItems = eclatInstance.run()
    
    rules = associationRule(freqItems, listOfItemInEachTransaction, minConf=minimumConfidenceRatio)
    
    # time.sleep(2) 
    end_time = time.time()
    execution_time = end_time - start_time

    # mining_process_id = eclatStoreMining(startDate, endDate, minimumSupport, minimumConfidence, rules, lenOfTransaction, execution_time)
    mining_process_id = 'test123'
    miningProcessIsExist = False
    miningProcess = MiningProcess.query.filter_by(id=mining_process_id).first()
    
    if miningProcess:
        miningProcessIsExist= True
        
    associated_rules_with_names = associateItemCodeWithName(rules=rules)
    
    return render_template("mining/eclat.html",
                           parameters=parameters,
                           verticalData=verticalData, 
                           lenOfTransaction=lenOfTransaction, 
                           miningProcessIsExist=miningProcessIsExist,
                           associated_rules=associated_rules_with_names,
                           mining_process_id=mining_process_id,
                           freqItems=freqItems,
                           execution_time=execution_time)
    

def fpGrowthIndex():
    return render_template("mining/fp-growth.html")


def fpGrowthMining():
    start_time = time.time()

    request_form = request.form.to_dict()
    startDate = request_form['start-date']
    endDate = request_form['end-date']
    minimumSupport = float(request_form['minimumSupport'])
    minimumConfidence = float(request_form['minimumConfidence'])
    
    parameters = {
        'startDate': startDate,
        'endDate': endDate,
        'minimumSupport': minimumSupport,
        'minimumConfidence': minimumConfidence
        }
    
    # transactions = Transaction.query.all()
    transactions_in_period = Transaction.query.filter(Transaction.date.between(startDate, endDate)).all()
    lenOfTransaction = len(transactions_in_period)
    if lenOfTransaction <=0:
        flash('Tidak ada transaksi pada periode tersebut.')
        return render_template("mining/fp-growth.html")
    
    minimumSupportFreq = (minimumSupport / 100) * len(transactions_in_period)
    minimumConfidenceRatio = minimumConfidence / 100
    
    # Algorithm here
    fpGrowthInstance = FPGrowth(minimumSupportFreq, 0.75)
    dictOfItemFrequency, filteredItemset, freqentItemset, listOfItemset, minimumConfidenceRes = fpGrowthInstance.run()
    
    rules = associationRuleFpGrowth(freqentItemset, listOfItemset, minConf=minimumConfidenceRes)
    
    # time.sleep(2) 
    end_time = time.time()
    execution_time = end_time - start_time
    
    # mining_process_id = eclatStoreMining(startDate, endDate, minimumSupport, minimumConfidence, rules, lenOfTransaction, execution_time)
    mining_process_id = 'test123'
    # mining_process_id = '2a863b34-2201-4003-b3d7-4c2535cc421b'
    miningProcessIsExist = False
    miningProcess = MiningProcess.query.filter_by(id=mining_process_id).first()
    
    if miningProcess:
        miningProcessIsExist= True
        
    associated_rules_with_names = associateItemCodeWithName(rules=rules)
    
    return render_template("mining/fp-growth.html",
                           parameters=parameters,
                           lenOfTransaction=lenOfTransaction,
                           dictOfItemFrequency=dictOfItemFrequency,
                           filteredItemset=filteredItemset,
                           miningProcessIsExist=miningProcessIsExist,
                           associated_rules=associated_rules_with_names,
                           mining_process_id=mining_process_id,
                           execution_time=execution_time)