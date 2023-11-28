from flask import render_template, request, redirect, url_for, flash
import time
from app import db
from src.models.transaction import Transaction, TransactionProduct
from src.models.product import Product
from src.mining_algorithms.eclat import Eclat
from src.mining_algorithms.fpgrowth import FPGrowth
from src.mining_algorithms.association_rule import associationRule, associationRuleEclatWithoutVerbose, associationRuleFpGrowth
from src.models.mining import MiningProcess, AssociationResult, AssociationResultProduct
import datetime
import uuid
from memory_profiler import profile


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
    
    sorted_rules = sorted(associated_rules_with_names, key=lambda x: x['confidence'], reverse=True)
    return sorted_rules


def formattingExecutionTime(execution_time):
    display_time = 0.0
    unit = ""
    
    if execution_time < 1:
        display_time = execution_time * 1000
        unit = "milidetik"
    elif execution_time < 60:
        display_time = execution_time
        unit = "detik"
    elif execution_time < 3600:
        display_time = execution_time / 60
        unit = "menit"
    else:
        display_time = execution_time / 3600
        unit = "jam"
    
    return display_time, unit
    

def eclatMining():
    start_time = time.time()

    request_form = request.form.to_dict()
    startDate = request_form['start-date']
    endDate = request_form['end-date']
    minimumSupport = float(request_form['minimumSupport'])
    minimumConfidence = float(request_form['minimumConfidence'])
    verbose = bool(request.form.get('verbose'))
    
    parameters = {
        'startDate': startDate,
        'endDate': endDate,
        'minimumSupport': minimumSupport,
        'minimumConfidence': minimumConfidence
        }
    
    lenOfTransaction = Transaction.query.filter(Transaction.date.between(startDate, endDate)).count()
    transactions_in_period = (
        db.session.query(TransactionProduct)
        .join(Transaction, TransactionProduct.transaction_id == Transaction.transaction_id)
        .filter(Transaction.date.between(startDate, endDate))
        .all()
    )
    
    if lenOfTransaction <= 0:
        flash('Tidak ada transaksi pada periode tersebut.')
        return render_template("mining/eclat.html")
    
    minimumSupportFreq = (minimumSupport / 100) * lenOfTransaction
    minimumConfidenceRatio = minimumConfidence / 100
    eclatInstance = Eclat(minsup=minimumSupportFreq, verbose=verbose)
    listOfItemInEachTransaction = eclatInstance.read_data(transactions_in_period)
    # verticalData, freqItems = eclatInstance.run()
    
    verticalData = {}
    freqItems = {}
    if verbose:
        result = profile(eclatInstance.run)()
        verticalDataRes, freqItemsRes = result
        verticalData = verticalDataRes
        freqItems = freqItemsRes
    else:
        result = profile(eclatInstance.run)()
        freqItemsRes = result
        freqItems = freqItemsRes

    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_res, execution_time_unit = formattingExecutionTime(execution_time)
    
    if verbose:
        rules = associationRule(freqItems, listOfItemInEachTransaction, minConf=minimumConfidenceRatio)
    else:
        rules = associationRuleEclatWithoutVerbose(freqItems, listOfItemInEachTransaction, minConf=minimumConfidenceRatio)

    # mining_process_id = eclatStoreMining(startDate, endDate, minimumSupport, minimumConfidence, rules, lenOfTransaction, execution_time)
    mining_process_id = 'test123'
    miningProcessIsExist = False
    miningProcess = MiningProcess.query.filter_by(id=mining_process_id).first()
    
    if miningProcess:
        miningProcessIsExist= True
        
    associated_rules_with_names = associateItemCodeWithName(rules=rules)
    
    
    if verbose:
        return render_template("mining/eclat.html",
                            parameters=parameters,
                            verticalData=verticalData, 
                            lenOfTransaction=lenOfTransaction, 
                            miningProcessIsExist=miningProcessIsExist,
                            associated_rules=associated_rules_with_names,
                            mining_process_id=mining_process_id,
                            freqItems=freqItems,
                            execution_time_res=execution_time_res,
                            execution_time_unit=execution_time_unit)
    else:
        return render_template("mining/eclat.html",
                            parameters=parameters,
                            lenOfTransaction=lenOfTransaction, 
                            miningProcessIsExist=miningProcessIsExist,
                            associated_rules=associated_rules_with_names,
                            mining_process_id=mining_process_id,
                            execution_time_res=execution_time_res,
                            execution_time_unit=execution_time_unit)
    

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