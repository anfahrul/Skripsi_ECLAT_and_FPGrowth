from flask import render_template, request, redirect, url_for, flash, Response
import time
from app import db
from src.models.transaction import Transaction
from src.models.mining import MiningProcess, AssociationResult, AssociationResultProduct
from src.models.product import Product
from fpdf import FPDF


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


def getMiningProcess(process_id):
    mining_process = MiningProcess.query.get(process_id)

    query = db.session.query(
        AssociationResultProduct.association_result_id,
        AssociationResultProduct.is_antecedent,
        AssociationResult.support,
        AssociationResult.confidence,
        AssociationResult.lift,
        Product.itemCode,
        Product.name.label("item_name")
    ).join(AssociationResult).join(
        Product, AssociationResultProduct.itemCode == Product.itemCode
    ).filter(AssociationResult.mining_process_id == process_id)

    results = query.all()

    associations = {}
    for result in results:
        association_id = result.association_result_id
        if association_id not in associations:
            associations[association_id] = {
                'antecedent': set(),
                'consequent': set(),
                'support': result.support,
                'confidence': result.confidence,
                'lift': result.lift,
            }
        if result.is_antecedent:
            associations[association_id]['antecedent'].add((result.itemCode, result.item_name))
        else:
            associations[association_id]['consequent'].add((result.itemCode, result.item_name))

    return mining_process, associations


def detailMiningProcess(process_id):
    mining_process, associations = getMiningProcess(process_id)
    
    print("mining_process", mining_process)
        
    return render_template('mining_history/detail_mining_history.html', mining_process=mining_process, associations=associations)


def generateReport(process_id):
    pdf = FPDF()
    margin_x = 15
    margin_y = 20
    pdf.set_margins(margin_x, margin_y)
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(page_width, 0.0, 'Sinar Mart', align='L')
    pdf.ln(5)
    pdf.set_font('Arial', '', 11.0)
    pdf.cell(page_width, 0.0, 'Jl. D.I Panjaitan No 88 A, Lepo - Lepo', align='L')
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12.0)
    pdf.cell(page_width, 0.0, 'LAPORAN HASIL ANALISIS ASOSIASI', align='L')
    pdf.ln(5)
    
    no_col_width = 10
    col_width_temp = (page_width - no_col_width)/4
    association_col_width = (col_width_temp * 2) - no_col_width
    col_width = (page_width - association_col_width - no_col_width)/3
        
    th = pdf.font_size
    
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(235, 235, 235)
    pdf.cell(no_col_width, th + 5, 'No.', border=1, align='C', fill=True)
    pdf.cell(association_col_width, th + 5, 'Aturan Asosiasi', border=1, align='C', fill=True)
    pdf.cell(col_width, th + 5, 'Support (%)', border=1, align='C', fill=True)
    pdf.cell(col_width, th + 5, 'Confidence (%)', border=1, align='C', fill=True)
    pdf.cell(col_width, th + 5, 'Nilai Lift', border=1, align='C', fill=True)
    pdf.ln(th + 5)
    
    pdf.set_font('Arial', '', 11)
    
    mining_process, associations = getMiningProcess(process_id)
   
    row_number = 1
    for association_id, association in associations.items():
        pdf.set_fill_color(255, 255, 255)

        antecedent_text = "\n".join([f"{item[0]} - {item[1]}" for item in association['antecedent']])
        consequent_text = "\n".join([f"{item[0]} - {item[1]}" for item in association['consequent']])
        combined_text = f"Jika membeli:\n{antecedent_text}\nMaka berpotensi membeli:\n{consequent_text}"

        # Calculate the height of the multi-cell content
        lines = combined_text.split('\n')
        multi_cell_height = (th + 2) * len(lines)
    
        # Nomor dan aturan asosiasi
        pdf.cell(no_col_width, multi_cell_height, str(row_number), border=1, align='C')
        
        currrent_x = pdf.get_x()
        currrent_y = pdf.get_y()

        pdf.multi_cell(association_col_width, th + 2, combined_text, border=1)
        
        # Support, confidence, dan lift
        pdf.set_xy(currrent_x + association_col_width, currrent_y)
        pdf.cell(col_width, multi_cell_height, str(association['support']), border=1, align='C')
        pdf.cell(col_width, multi_cell_height, str(association['confidence']), border=1, align='C')
        pdf.cell(col_width, multi_cell_height, "{:.2f}".format(association['lift']), border=1, align='C')

        # Pindah ke baris berikutnya
        pdf.ln()
        
        currrent_x = pdf.get_x()
        currrent_y = pdf.get_y()
        pdf.set_xy(currrent_x, currrent_y)
        

        row_number += 1


    pdf.ln(10)
    
    
    pdf.set_font('Times', '', 10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment; filename=mining-report.pdf'})


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