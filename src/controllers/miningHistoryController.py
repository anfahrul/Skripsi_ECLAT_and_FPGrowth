from flask import render_template, request, redirect, url_for, flash
import time
from app import db
from src.models.transaction import Transaction
from src.models.mining import MiningProcess, AssociationResult, AssociationResultProduct
from src.models.product import Product


def historyIndex():
    mining_process = MiningProcess.query.all()
    
    return render_template("mining_history/history_index.html", mining_process=mining_process)


def deleteMiningProcess(process_id):
    mining_process = MiningProcess.query.get(process_id)

    if mining_process:
        db.session.delete(mining_process)
        db.session.commit()
        print(f"Data mining process dengan ID {process_id} telah dihapus.")
    else:
        print(f"Data mining process dengan ID {process_id} tidak ditemukan.")
    
    return redirect(url_for('mining_history_blueprint.mining_history'))
    

def detailMiningProcess(process_id):
    mining_process = MiningProcess.query.get(process_id)
    
    query = db.session.query(
        AssociationResultProduct.association_result_id,
        AssociationResultProduct.is_antecedent,
        AssociationResult.support,
        AssociationResult.confidence,
        AssociationResult.lift,
        Product.name.label("item_name")
    ).join(AssociationResult).filter(AssociationResult.mining_process_id == process_id)

    query_antecedent = query.join(Product, AssociationResultProduct.itemCode == Product.itemCode)
    query_consequent = query.join(Product, AssociationResultProduct.itemCode == Product.itemCode)

    results_antecedent = query_antecedent.filter(AssociationResultProduct.is_antecedent == True).all()
    results_consequent = query_consequent.filter(AssociationResultProduct.is_antecedent == False).all()

    associations = {}
    for result_antecedent in results_antecedent:
        association_id = result_antecedent.association_result_id
        if association_id not in associations:
            associations[association_id] = {
                'antecedent': set(),
                'consequent': set(),
                'support': result_antecedent.support,
                'confidence': result_antecedent.confidence,
                'lift': result_antecedent.lift,
            }
        associations[association_id]['antecedent'].add(result_antecedent.item_name)

    for result_consequent in results_consequent:
        association_id = result_consequent.association_result_id
        associations[association_id]['consequent'].add(result_consequent.item_name)
        
    
    return render_template('mining_history/detail_mining_history.html', mining_process=mining_process, associations=associations)


# def detailMiningProcess(process_id):
#     mining_process = MiningProcess.query.get(process_id)
    
#     query = db.session.query(
#         AssociationResultProduct.association_result_id,
#         AssociationResultProduct.itemCode,
#         AssociationResultProduct.is_antecedent,
#         AssociationResult.support,
#         AssociationResult.confidence,
#         AssociationResult.lift,
#         # Product.itemCode.label("product_item_code")
#     )

#     # Bergabung dengan tabel AssociationResult untuk mendapatkan support, confidence, dan lift
#     query = query.join(AssociationResult, AssociationResultProduct.association_result_id == AssociationResult.id)

#     # Bergabung dengan tabel Product untuk mendapatkan itemCode dari produk terkait
#     query = query.join(Product, AssociationResultProduct.itemCode == Product.itemCode)

#     # Menambahkan filter berdasarkan mining_process_id
#     query = query.filter(AssociationResult.mining_process_id == process_id)

#     # Eksekusi query dan ambil hasilnya
#     results = query.all()
    
#     associations = {}
#     for result in results:
#         association_id = result.association_result_id
#         if association_id not in associations:
#             associations[association_id] = {
#                 'antecedent': set(),
#                 'consequent': set(),
#                 'support': result.support,
#                 'confidence': result.confidence,
#                 'lift': result.lift,
#             }
#         if result.is_antecedent:
#             associations[association_id]['antecedent'].add(result.itemCode)
#         else:
#             associations[association_id]['consequent'].add(result.itemCode)
    
#     return render_template('mining_history/detail_mining_history.html', mining_process=mining_process, associations=associations)